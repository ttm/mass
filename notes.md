SI:
* arrumar a ordem das figuras (fig 3 trocou com a 4)
* add the Doppeleer; Re-verb pieces.
* add the functions.py and hrtf.py scripts. (assert that they are in the body of the text)

Scripts:
* change f_a to f_s or fs
* match script names of pieces from listing to source tree.
* add script on images for transitions ????
* Divide sound by max(max, -min) in normalization
* Include movement(2).py (in a sandbox?) or remove it.
* Make Doppler with transitions of pitch, of location and vibratos OK
* Make arbitrary movements. OK
* homogeneize names of rendered wav files
* convolve noises and rhythms in the frequency domain
* arrumar implementacao da dente de serra
* assure the scripts are running (e.g. because it uses a sound sample)
* Make Doppler right! And a musical piece.
* Make the Re-verb piece!
* Make a piece using HRTF, maybe make it also using ITD and IID to compare.
* Arrumar Acorde cedo para fazer modulacoes
* Incorporate fractalize.py
* Model the sonic boom (when the moving source reaches the sonic speed)
* Make a piece with noises that use the same bandwidth as harmonies
or notes.

Body:
* position figures
* see if codes.pdf is not dropping out of the margin
* figgus package is very preliminary. Its principles are incorporated into music. It is interesting because:
  - It does use MASS but does not require numpy to render sonic arrays and write WAV files
  - Implements a whole EP album.
  - Inherits the original FIGGUS concepts (articles)
  - Is a step betwen original FIGGUS and the music package
* Mention that this work was called music in digital audio: psychophysic description and toolbox
* Cite more reference works that I've visited (from CCRMA, UPF, Brazil, England, Germany, IRCAM, etc)
* Add about the functions implemented.
* Very easy to inspect and assure the sound is what you expect it to be, in terms of the most used variables in physichophysics.

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
* Make a final musical suite using the techniques presented?

Extra:
* How much is the deviation of the notes in the
equal temperament from the natural tuning (harmonic series)?
chromatic scale to the harmonic series?
* avisar Cristina que coloquei o número do projeto no trabalho.
* send work to numpy/scipy community
* Is PCM audio representing the displacement or the pressure variation?
* Use numpy's system to obtain HTML representation of the documentation in music package.
* Send notes on the implementations of HRTF to email lists.
* send to LAD the functions on localization:
  - being frequency dependent (loc\_())
  - and using HRTF while the source is moving (movingHRTF())
* Ask about LUT:
	- 44100/1024 ~ 43Hz, the table should be bigger
	- For control variables (such as a vibrato) the frequency can be very small, such as .3hz
	- Is it really ok to use 1024?
	- No interpolation needed for the indexes?
* Avisar music-dsp q citei eles na secao de filtros
* Ask around about the power variation in the Doppler effect
