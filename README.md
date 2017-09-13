# mass
MASS (Music and Audio in Sample Sequences) is a mathematical and computational framework relating musical elements to PCM audio samples

### structure of this repository

* the doc/ directory holds the:
  - article.pdf which describes the MASS framework.
  - listings.pdf which displays lists of:
    * sections, figures and tables of the article;
    * scripts that implement the equations, musical pieces and figures;
    * auxiliary scripts;
    * tables.
  - tex files that are used to render these PDFs.
* The src/ directory holds Python scripts:
  - src/sections/ holds the scripts that implement the equations in each of the sections of the articles.
  - src/aux/ holds scripts that render the figures in the article and other auxiliary scripts.
  - src/aux/filters/ holds auxiliary scripts related to IIR and FIR filters.
  - src/pieces2/ holds scripts that render the musical pieces using the resources described in the second section of the article.
  - src/pieces3/ holds scripts that render the musical pieces using the resources described in the third section of the article.
  - src/pieces4/ holds scripts that render the musical pieces using the resources described in the fourth section of the article.

### related work
This work is heavely influenced by this [MSc dissertation](http://www.teses.usp.br/teses/disponiveis/76/76132/tde-19042013-095445/publico/RenatoFabbri_ME_corrigida.pdf).

And the code and documentation available at [this repository](https://github.com/ttm/dissertacao/).

The dissertation have been translated into English, enhanced
and formatted as an article.
The code has been reorganized.
All these items are in this repository.
The Appendices of the dissertation still have important information:
* Appendix G holds information on related books and articles: descriptions,
how they differ from and complement this work.
* Appendix F holds descriptions of projects that were performed using the MASS framework.
* Appendix D holds considerations about AM and FM performed with logarithmic oscillations.
