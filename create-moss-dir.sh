n=3
mkdir ~/lab${n}s
ls -d * > ../lab${n}s
for x in $(cat ../lab${n}s); cp $x/lab${n}/lab${n}.asm ~/lab${n}s/$x.asm

# cd into spring repos and run
n=3
ls -d * > ../lab${n}s
for x in $(cat ../lab${n}s); cp $x/lab${n}/lab${n}.asm ~/lab${n}s/SPRING_2020/$x.asm