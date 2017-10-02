* change f_a to f_s or fs
* render PDF with code (and reference it in the article)
* add PPEPPS as a reference (figgus repo)
* see notes on the other laptop
* How much is the deviation of the notes in the
chromatic scale to the harmonic series?
* synonym: semitone and half step
* avisar Cristina que coloquei o número do projeto no trabalho.
* License: public domain?
* position figures
* see if codes.pdf is not dropping out of the margin
* make soundcloud playlists of songs: by section, extra, all
* match script names of pieces from listing to source tree.
* include aux/utils.py to listings
* send work to numpy/scipy community
* add notes:
  - sample-based synthesis, meaning methods where each sample is calculated indivudally. Usually not fit for real-time, but fidelity of sound wave to the mathematical models is maximized.
* figgus package is very preliminary. Its principles are incorporated into music. It is interesting because:
  - It does uses MASS but does not require numpy to render sonic arrays and write WAV files
  - Implements a whole EP album.
  - Inherits the original FIGGUS concepts (articles)
  - Is a step betwen original FIGGUS and the music package
* add script on images for transitions
* review loudness transitions to verify if is according to exponential transitions.
* find words logarith... to see if needs to be replaced by exponential
* Make song on spatialization
* Divide sound by max(max, min) in normalization
* Two advantages of the ITD and IID described:
  - It is true to the physical phenomena of sound propagation:
    - Disconsiders HRTF.
  - It is easy to model and make hacks (e.g. transitions)
* Linear PCM
* Is PCM audio representing the displacement or the pressure variation?
* Include movement(2).py (in a sandbox?) or remove it.
* Make Doppler with transitions of pitch, of location and vibratos
* Make arbitrary movements.
* Use numpy's system to obtain HTML representation of the documentation
in music package.
* Homogenize linear and lin
* Put note on a golden rule: if your sound has variations of pitch,
they need to be accounted for befor making the table lookup because
it relies on the frequency.
* Refazer ADa e SaRa? bonds? Melhorar trenzinho? Vibra e treme (subst pelo art on vibratos?)?
* deixar somente o ruidosa faixa 4
* homogeneize names of rendered wav files
* Implement usage of HRTF
  - from webaudioapi?
  - NPHRTF is also generalized HRTF
  - CSound uses MIT: 
* convolve noises and rhythms in the frequency domain
* arrumar figura e definicao de convolucao no artigo
* send to LAD the functions on localization:
  - being frequency dependent (loc\_())
  - and using HRTL while the source is moving (movingHRTF())
