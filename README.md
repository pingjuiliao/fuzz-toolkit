# Fuzzing toolkits
- American Fuzzy Lop (AFL)
- Qsym
- other scripts

## setup
Build AFL docker
```
cd AFL-master && docker build -t afl/afl-fuzz .
```

say you have a machine dedicated for fuzzing, add bin to the path
```
export PATH=${PATH}:$(pwd)/bin
```

## Usage
Build the binary: we leave AFL-gcc here


One-instance fuzzing
```
afl-docker.py -i ./in_dir -o ./out_dir -p ./program.exe
```
