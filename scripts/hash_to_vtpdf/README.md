# hash_to_vtpdf.py

## Purpose
Takes a list of sha256 hashes and will get the VirusTotal behavior tab for the each file specificed by the hash and save it as a pdf in the output directory specified

## Usage
```
python hash_to_vtpdf.py <SHA256 hash file> <OUTPUTDIR>
```

The SHA256 hash file will have the following format:
```
359110e45e6469b71d4ac5401546cf347c9e824ee6423d9864fa69fd435ae6be  evade2_S5/0000_s5
5ea8647d7e895547bfa2f102544cabca7e21dc9763455a41f665acffc7589a82  evade2_S5/0001_s5
ddef1281efdf512ab65d352bfa8f806975769f9e2b990577b9cc1e7bfb6b4e10  evade2_S5/0002_s5
163b47342b11284df918ff07b33562847f8d32d8e7300a509e746373336b50c2  evade2_S5/0003_s5
31758c05555c2f06a7649f98b384b7b0a4c1f0a4e52da19bee370648f6b91c18  evade2_S5/0004_s5
7b5f75e1fd5f4f6dc70b8a69d5a08c55e0e239d50d527cd2d6de751cde7f1596  evade2_S5/0005_s5
1f46e0a5eb83b3d81b503e45dd49d2fa7ad2c33d656c610d2cf8d6dac1bd39a3  evade2_S5/0006_s5
```
