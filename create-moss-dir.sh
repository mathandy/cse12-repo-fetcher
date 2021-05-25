# ###
# These snippets are meant to be copy/pasted!
# ###
exit

n=3
term="s21"
OUTDIR="~/lab${n}s-$term"
mkdir $OUTDIR
cd repos | echo "ERROR" & exit
ls -d * > ../lab${n}s.txt
for x in $(cat ../lab${n}s.txt); cp $x/lab${n}/lab${n}.asm "$OUTDIR"/$x.asm

# cd into spring repos and run
n=3
term="s21"
OUTDIR="~/lab${n}s-$term"
cd repos
ls -d * > ../lab${n}s
for x in $(cat ../lab${n}s); cp $x/lab${n}/lab${n}.asm "$OUTDIR"/SPRING_2020/$x.asm

perl ~/moss.pl -l mips {F20/*,*.asm}
perl ~/moss.pl -l mips *.asm
perl ~/moss.pl -l mips {F20/*,S20/*,*.asm}