# Machine-voter-lectronique_Python
Le but de ce projet informatique est de vous faire créer une simulation de machine à voter securisé. La principale limitation du projet réside dans le fait que, dans un contexte opérationel, plusieurs entité distante et distincte doivent être impliquée ; dans notre projet les entités seront toutes hébergés sur le même ordinateur hôte.

# Rapport 

Ce rapport est écrit pour présenté brièvement le projet. 

## Diffcultés rencontrées

* Zero-knowledge Proof
  Nombres trop large pour calculer, même si on utilise l'exponentiel rapide

## Solutions mise en oeuvre

* Singleton
```py
def singleton(classe):
    _instance = {}

    def inner():
        if classe not in _instance:
            _instance[classe] = classe()
        return _instance[classe]

    return inner

```

## Details

1. Trouver Zp et son générateur 
    Dans le document de Belenios...

2. Génération d'UUID
    utiliser la façon HASH (sha256). fichier `pythonSHA256.py`
    ```py
    def generate_uuid(self, x):
        return generate_hash(x.nom + x.prenom).hex()
    ```

3. Génération de Cn et Pub(Cn)
    fichier `Credential.py`, `PBKDF2.py` et `HmacSHA256.py`
    ```py
    def generate_intern_cn(self, x):
        crediential = Credential()
        return crediential.get_cn()

    def generate_pub_cn(self, x):
        crediential = Credential()
        return crediential.generate_pubcn(x.cn, x.uuid)
    ```

    - Génération de Cn
      faire référence au docu Belenios
      14 lettres aléatoires et un lettre comme checksum

    - Génération Pub(Cn)
      comme l'indique dans le cahier de charges
      utiliser les fonctions dans les fichiers `Credential.py`, `PBKDF2.py`

  4. `Shuffle`
      fichier `Algorithme/Shuffle.py`

  5. Communication : `BlowFish` Chiffrement symétrique
      fichier `Chiffrement/BlowFish.py`
      ```py
      # exemple
      driver_init()
      a = input_string("exemple blowfish")
      print(a)
      print(return_string(a)) # exemple blowfish
      ```

  6. Certificats : Ca, Ce, Cs pour les trois serveurs existants
      fichier `entities/autoriteConfiance.py`
      utiliser un string secret comme `certificate = "Server-Enregistrement"` et le chiffrement asymétrique ElGamal `Chiffrement/ElGamal.py`
      ```py
      def test():
        keys = generate_keys()
        priv = keys['privateKey']
        pub = keys['publicKey']
        message = "My name is li. "
        cipher = encrypt(pub, message)
        plain = decrypt(priv, cipher)

        return message == plain
      ```
      vérifier un certificat
      ```py
      def check_certificate_admin(self, cipher):
        plaintext = elgamal.decrypt(self.keys_admin["privateKey"], cipher)
        if plaintext != self.message_admin:
            raise "Server Administartion is not qualified !"

        print(Fore.GREEN + Style.BRIGHT + "Server Administration's certificate has been checked !" + Style.RESET_ALL)
      ```

  7. Générations des clés de V1, V2, ..., Vn
      ElGamal + une somme de clés secrète
      fichier `entities/Trustee.py`
      ```py
      def generate_keys(self):
        ...
        h = elgamal.modexp(g, self.number_sum_s, prime_alea)
        iNumBits = 256
        self.publicKey = elgamal.PublicKey(prime_alea, g, h, iNumBits)
        self.privateKey = elgamal.PrivateKey(prime_alea, g, self.number_sum_s, iNumBits)
      ```  
      utiliser la même façon comme cerficats pour vérifier les identités de Trustees au début de l'élection

  8. Contenu de bulletin
     - Chiffrement de la vote 
        utiliser la clé publicque de Trustee pour chiffrer la vote d'un voter
     - Zero-knowledge Proof
        faire exactement comme celui indiqué dans le cahier des charges
        
