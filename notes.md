SI:
* arrumar a ordem das figuras (fig 3 trocou com a 4)
Scripts:
* change f_a to f_s or fs
* match script names of pieces from listing to source tree.
* include aux/utils.py to listings
* add script on images for transitions
* Divide sound by max(max, min) in normalization
* Include movement(2).py (in a sandbox?) or remove it.
* Make Doppler with transitions of pitch, of location and vibratos
* Make arbitrary movements.
* homogeneize names of rendered wav files
* convolve noises and rhythms in the frequency domain
* arrumar implementacao da dente de serra
* assure the scripts are running (e.g. because it uses a sound sample)

Body:
* synonym: semitone and half step
* position figures
* see if codes.pdf is not dropping out of the margin
* figgus package is very preliminary. Its principles are incorporated into music. It is interesting because:
  - It does use MASS but does not require numpy to render sonic arrays and write WAV files
  - Implements a whole EP album.
  - Inherits the original FIGGUS concepts (articles)
  - Is a step betwen original FIGGUS and the music package
* review loudness transitions to verify if is according to exponential transitions.
* find words logarith... to see if needs to be replaced by exponential
* Two advantages of the ITD and IID described:
  - It is true to the physical phenomena of sound propagation:
    - Disconsiders HRTF.
  - It is easy to model and make hacks (e.g. transitions)
* Linear PCM
* Put note on a golden rule: if your sound has variations of pitch,
they need to be accounted for before making the table lookup because
it relies on the frequency.
* Generalized/non-personalized HRTF.
* arrumar figura e definicao de convolucao no artigo
* adicionar que no sinal discreto n ha derivadas e integrais
* Further describe the captions of the figures (e.g. fig 3)

Musical pieces:
* make soundcloud playlists of songs: by section, extra, all
* Make song on spatialization
* Homogenize linear and lin
* Refazer ADa e SaRa? bonds? Melhorar trenzinho? Vibra e treme (subst pelo art on vibratos?)?
* deixar somente o ruidosa faixa 4
* make list of musical pieces done with mass in a wiki page
* add about the implementations with HRTF in the sec 3:
maybe make a musical piece using only IID and ITD
and using HRTFs.

Extra:
* How much is the deviation of the notes in the
equal temperament from the natural tuning (harmonic series)?
* avisar Cristina que coloquei o número do projeto no trabalho.
chromatic scale to the harmonic series?
* send work to numpy/scipy community
* Is PCM audio representing the displacement or the pressure variation?
* Use numpy's system to obtain HTML representation of the documentation in music package.
* Send notes on the implementations of HRTF to email lists.
* send to LAD the functions on localization:
  - being frequency dependent (loc\_())
  - and using HRTF while the source is moving (movingHRTF())
