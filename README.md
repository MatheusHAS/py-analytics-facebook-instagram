# py-analytics-facebook-instagram
Software foi desenvolvido com intuito de mapear os dias da semana, em que as fotos foram mais curtidas, tanto no facebook quanto no instagram. Essa solução foi desenvolvida como forma de estudo da linguagem Python.

### Requisitos
* Python 3.6+


### Sintaxe de Uso
```
py run-analytics.py -tkf TOKEN_DO_FACEBOOK -tki TOKEN_DO_INSTAGRAM -f NOME_DOS_ARQUIVOS
```

### Arquivo de Dados
**Facebook:**
```
DATA-DO-POST|DATA-FORMATADA-UTC|DIA-DA-SEMANA|ID_DO_POST|LIKE|LOVE|HAHA|WOW|SAD|ANGRY
```
* 0 => Data do Post
* 1 => Data do Post formatado em UTC
* 2 => Dia da Semana (SEG|TER|QUA|QUI|SEX|SAB|DOM)
* 3 => ID da postagem
* 4 => Like - Curtidas
* 5 => Love - Amei
* 6 => HAHA - Haha
* 7 => WOW - Wow
* 8 => SAD - Triste
* 9 => ANGRY - Angry

**Instagram:**
```
DATA-DO-POST|DATA-FORMATADA-UTC|DIA-DA-SEMANA|ID_DO_POST|LIKE
```
* 0 => Data do Post
* 1 => Data do Post formatado em UTC
* 2 => Dia da Semana (SEG|TER|QUA|QUI|SEX|SAB|DOM)
* 3 => ID da postagem
* 4 => Like - Curtidas

Após executar o py analytics, todos os dados obtidos estaram em 2 locais. Na pasta 'GRAFICOS' encontramos todos os gráficos gerados utilizando arquivos do Excel (XLS). Já na pasta 'DADOS' existem os dados separados por 'Pipe'.

### Obter Token do Instagram (forma rápida):
Pode ser obtido através do Link:
* [http://instagram.pixelunion.net/](http://instagram.pixelunion.net/)

### Obter Token do Facebook 
Pode ser obtido através do link:
* [https://developers.facebook.com/tools/explorer/](https://developers.facebook.com/tools/explorer/)

**Desenvolvido com fins acadêmicos.**

### License
GNU General Public License

### Desenvolvedores
* **Matheus Azambuja** - [<matheushenrique.ads@gmail.com>](matheushenrique.ads@gmail.com)
* **Geisiane Araujo** - [<geisiane.aa@gmail.com>](geisiane.aa@gmail.com)