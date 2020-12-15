n=5
mkdir ~/lab${n}s
ls -d */ > ../lab${n}s
for x in $(cat ../lab${n}s); cp $x/lab${n}/lab${n}.asm ~/lab${n}s/$x.asm