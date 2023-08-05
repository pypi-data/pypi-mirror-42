import argparse, os.path, re, sys

__all__ = ('regs',)

_par = re.compile(r'(.+?\n)\n\[', re.S).match
_key_values = re.compile(r'(.+?)\]\n(.*)', re.S).match
_value_data = re.compile(r'(?:@|"(.+?)")=(".*?(?<=\\)"|.+?[^\\])\n', re.S).findall

def regs(*files, flags=''):
	if len(files) < 2:
		print('needs at least 2 files', file=sys.stderr)
		return 1
	binary_, color_, show_ = 'b' in flags, 'n' not in flags, 'q' not in flags
	def show(key, value=None, data=None):
		if show_:
			key = (key
				.replace('HKEY_CLASSES_ROOT','HKCR')
				.replace('HKEY_CURRENT_USER','HKCU')
				.replace('HKEY_LOCAL_MACHINE','HKLM')
				.replace('HKEY_USERS','HKU')
				.replace('HKEY_CURRENT_CONFIG','HKCC'))
			if not data:
				print(key)
			elif binary_ or not data.startswith('hex:'):
				color = (1 if data.startswith('hex:') else
					2 if data.startswith('"') else
					4 if data.startswith('dword:') else
					5 if data.startswith('hex(b):') else
					6 if data.startswith('hex(0):') else 3) if color_ else None
				print(f'{key}\\' + (f'\033[1;3{color}m{value}\033[m' if color else value))

	regs = []
	for file in files:
		if not os.path.exists(file):
			print(f'missing {repr(file)}', file=sys.stderr)
			return 1
		with open(file, encoding='utf-16') as f:
			text = f.read()
		if not text.startswith('Windows Registry Editor Version 5.00\n\n['):
			print(f'{repr(file)} is not a reg file')
			return 2
		regs.append([text + '\n\n[', text.index('[') + 1, len(text)])

	def par(reg):
		match = _par(reg[0], reg[1])
		if match:
			reg[1] = match.end()
			return match[1]

	def next_par():
		nonlocal pars
		pars = [par(r) for r in regs]

	next_par()
	while all(pars):
		if len(set(pars)) == 1:
			next_par()
		else:
			pars = [_key_values(p).groups() for p in pars]
			keys = [p[0] for p in pars]
			while all(pars) and len(set(keys)) > 1:
				min_k = min(keys, key=str.casefold)
				show(min_k)
				for i in range(len(regs)):
					if keys[i] == min_k:
						p = par(regs[i])
						pars[i] = p and _key_values(p).groups()
						keys[i] = p and pars[i][0]
			if all(pars):
				vds = [p[1] for p in pars]
				if len(set(vds)) > 1:
					key = pars[0][0]
					vds = [set(_value_data(vd)) for vd in vds]
					for v,d in dict(sorted(
							set.union(*vds) - set.intersection(*vds))).items():
						show(key, v, d)
				next_par()
	keys = []
	while any(pars):
		keys += [_key_values(p)[1] for p in pars if p]
		next_par()
	for k in sorted(keys, key=str.casefold):
		show(k)

def main():
	a = argparse.ArgumentParser(None, 'regs [-h] [-bnq] file ...', 'Compare Registry 0.1')
	a.add_argument('file', nargs='*', help='*.reg to compare')
	a.add_argument('-b', '--binary', action='store_true', help='show REG_BINARY')
	a.add_argument('-n', '--no-color', action='store_true', help='no ANSI colors')
	a.add_argument('-q', '--quiet', action='store_true', help='no output')
	args = a.parse_args()
	if args.file:
		return regs(*args.file,
			flags=''.join([x[0] for x in ('binary', 'no_color', 'quiet') if getattr(args,x)]))
	a.print_help()

if __name__ == '__main__':
	exit(main())