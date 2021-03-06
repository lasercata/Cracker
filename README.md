# Cracker
A useful software about cryptography, numbers and passwords.

![Cracker](Style/Cracker_ascii_logo_surrounded.png)

Cracker is a software developed and updated by Lasercata and by Elerias. It is written in Python 3 and in C.

This software is a toolbox application that allow you to do many things : you can encrypt
securely a secret message using one of the many ciphers presents in Cracker (KRIS, AES, RSA, ...),
sign it with a hash function, decrypt it. It is compatible with [KRIS](https://github.com/lasercata/KRIS) software.

If you have a message without the key, but you need to read the content, you can try to
crack it using a wordlist that you made with Cracker, or let the algorithm try to crack
it using its wordlist bank.

You don't remember which was your favourite wordlist ? Don't worry ! You can analyze
them with the wordlist tab to get numerous informations on them.

You need to convert a number from binary to hexadecimal ? You need to do a special convertion
using your own base alphabet ? Check the "Base convert" tab.

As you can see, there is a lot of functions, often about cracking. But Cracker
can also help to improve your security : if you need a strong password, hard to be
cracked by brute-force, the "P@ssw0rd_Test0r" tab is for you ! It gives a lot of informations
about the password you entered, like its entropy.


## Requirements

To run the software, you need to have :

* [Python3](https://www.python.org/downloads/)
* [PyQt5](https://pypi.org/project/PyQt5/)


## Installing

Download or clone the repository :

```bash
git clone https://github.com/lasercata/Cracker.git
```

Then unzip the wordlists :

```bash
cd Data/Wordlists
7z x wordlists.7z
rm wordlists.7z

cd ../..
```

If your are on Linux, you can alias the launchers : put these commands in the file `~/.bash_aliases` or `~/.bashrc` :

```bash
alias cracker='old_dir=$(pwd) && cd path/to/Cracker && ./Cracker_gui.py && cd $old_dir'
alias crackerc='old_dir=$(pwd) && cd path/to/Cracker && ./Cracker_console.py && cd $old_dir'
```

Make the launchers executable :

```bash
chmod +x *.py
```


## Running

### Run
For the graphical UI, run `./Cracker_gui.py` in the root of the project, or `cracker` anywhere if you added the aliases ;

For the console UI, run `./Cracker_console.py` in the root of the project, or `crackerc` anywhere if you added the aliases.

### Password
The default for application lock password is **`swiss_knife`**. 

You can change the password in the Settings part.


## RSA keys
You can manage RSA keys in the Cipher tab (with the buttons at right). You can generate new ones, get info on them, export or import public keys, ...

The default location for the keys is the folder `Cracker/Data/RSA_keys`. It is useful if you transport Cracker on a usb stick. But if you use it only on your computer, you can activate the `home` mode, meaning that the keys will be copied in the folder `~/.RSA_keys`. This is useful if you also use [KRIS](https://github.com/lasercata/KRIS) with `home` mode, or different versions of Cracker or KRIS (you won't have to copy the keys).

The `home` mode can be activated in the settings part.


## Authors

* **Lasercata** - [Lasercata](https://github.com/lasercata)
* **Elerias** - [Elerias](https://github.com/EleriasQueflunn)


## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details
