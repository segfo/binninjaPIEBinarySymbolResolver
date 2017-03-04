# binninjaPIEBinarySymbolResolver
resolve test binary  
echo "main(){printf(\"hello\");}" > test.c ; gcc -m32 -shared test.c -o sharedBinary  
