necessary:
- unify the mentions to scripts and musical pieces. E.g. only sec 2 starts by saying about it.
E.g. Sec 3 mentions the musical pieces not only on the end.

Urgent:
* Better discuss Midi notation, translation between midi and Hz
* make V() that oscilattes and in the pan
* Write about 60 beats/minute is the 'right tempo'.


Music package
* Recycle and document the IteratorSynth in music/sandbox/fourthChant.py
* 



pieces:
* Make thematic music: Christmas, anniversary, hollowing, wedding,
  newborn, new job, relationship anniversary or arbitrary
  commemoration. Referecess:
  https://www.youtube.com/watch?v=GPATUFiWoTI
* final suite as planned
* one or two routines for synthesizing albums:
  - with no parametrization
  - with arbitrary parametrization
* D\_(method=['exp']) is not working
* start piece with two voices, one speaking English and
the other in Toki Pona:
"""
English: MASS is useful for computer music,
Toki Pona: MASS li pona tawa kalama musi pi ilo nanpa.
English: You can sonify ideas, data and arbitrary structures into music,
Toki Pona: sina ken pali kalama kepeken nasin anu ijo ante.
"""
* use peals and rotations to walk on the scales.
  - Fast walks.
  - Slow upwards walk starts on the bass.
  - Gets responded by the treble in a slow downward walk.
  - Use of different symmetric scales as in trio 3
* Final piece:
  - name: SSSS (((symmetric suite) suite) suite) suite
    - 1st movement: Peal, better explore vibratos, tremolos and envelopes.
                    Maybe use the tentative coda for an interlude
                    between 5th and 6th movements.
                    Include something very probabilistic.
    - 2nd movement: Walk
    - 3rd movement: triangle and square
    - 4th movement: the circle
      - explore tremolos, vibratos, pan, DTI, IIT, doppler and HRTF
      - oscilation of filter settings, noise bandwidth, proportion
      of each waveform in a wavetable synthesis routine
      - oscilation of spectral components for inverse Fourier or
        wavelet transform
      - dihedral groups with many elements (specially rotations)
      - recalls 3rd movement on the end to bridge to 5th movement
    - 5th movement: peals, triangles, squares, circles and walks
    - 6th movement: spectra
      - Counterpoint of loudness:

        also, 10**(x/12) - n.log10(2**(y/12))
        i.e. the association of double pitch to y semitons (unknown?)
        (double frequency is associated with the same distance in
        pitch, but what is the interval of pitch y (or frequency) so that 
        a sound is perceived as twice as higher?

        2**(21/12) ~ n.log2(10),
        i.e. the convention of associating 10 dB to a double volume
        suggests that double the intensity of the sensation
        is related to 21 semitones = 12 + 9 = one octave and a major sixth.

        It seems ok because it is so subjective and dependent on the
        sound and context.

        21 semitons is close to two octaves, therefore, given that
        the convention of 10dB is very arbitrary, one might reason
        that neighbor octaves are not as easely associated with
        double pitch, but the second octave is.
    - 7th movement: samba
    - 8th movement: coda with data sonification and singing
    - Synthesize excerpts with fs >> 100kHz for using as wavetable
      * if s1_ is in fs=44100*4, we might obtain the same pitches
      is fs=44100 with s1_, s1_[::2] and with other indexes (as LUT)
      the resulting sound in fs is better quality.
      Use this feature to make a high quality freeze and stretch.
    - Implement Figgus as a function to ease granular and unit synthesis
    - Make some sort of tonal/modal harmony where voices might follow
      chords and scales, make the walks, and put some folcloric/ethnic
      melodies and rhythms.
        - Use triads and thetrads
        - Use chords of seconds and fourths, as well as of thirds
        - Develop the counterpoint to the extent where:
          * A second voice is built in accordance with a cantus firmus
          * The second voice, and/or the cantus firmus, might have an arbitrary rhythm input by
            user
          * The rules are all named, documented and configured to be
            respected or not.
          * Arbitrary rules are then easy to be added. The
            Counterpoint class always runs self.rulesCheck()
            after a note pitch/frequency and duration is 
          * Use loudness also to move voices independently.
          E.g. l = [a0*10**(i/12) for i in range(12)],
          l is multiplicative factors to the note sample amplitude:
          H(s*l[0]+s*l[7], s*l[2]+s*l[9])  # <= is a parallel perfect
          consonant (of a perfect 5th)
            - a_i ~ a0*10**(i/12) ~ a0*2**(1/12)
          * Tunable counterpoint interface.
          * Only uses pitch and duration
          * Handles arbitrary number of voices.
            - If voice precedence leaves it without possible moves,
              the note is just repeated.
           
* Make pieces with Daime Hymns.
  - Portuguese and Toki Pona (and english translation)
  - Cruzeirinho:
    * 06 mamaezinha
    * 11 flecha ligeira
  - o ebó audiovisual: sequência de hinos.
  - um ebó, ebós: hinos intercalados com outras peças,
  ou sequencias 
  - Puxar rezas em Toki Pona: ler/ouvir o hinário cantando.
  Versão do video com e sem escritos com o híno.
* Make Figgus (Finite groups in granular and unit synthesis)
  - Send to Ircam to the brazilian professor from near Jundiaí.
  - Implement it all! But no gui in emphasys.
  - It will be the core system that runs over the music python
    package that is based on MASS.
  - Write by heart without consulting software engineering,
  math, music, and other literature.
  - See some MOOCs, specially soft eng
  - Write about the advantages and losses of programming it
  without prior preparation.
  See if I am able to sustain an antithesis of the common place
  idea that planning beforehand is better. Reasons why it is not:
    * If you do something significant beforehand, it is more likely
    that you do somethings in a new or relevant way to given
    literature in the sense that you are not already formatted before
    thinking seriously on the subject.
    * You are most probably be able to enhance your work greatly
    after skimming through the literature.
    * Prof. Dr. L. da F. Costa sometimes mentions that he finds
    it a good habit to first find something of interest, then
    start digging with the tools at hand for something relevant.
    After things are reasonably interesting, and the discourse
    and a document is +- stable,
    then start digging literature (including videos and software).
    * Of course, there is some consideration of the literature
    on the whole process. And there is also background knowledge.
    E.g.: for this document on making the definitive Figgus,
    I wrote a preliminary version of it ~10 years ago,
    am finishing a article on the MASS (music and audio in PCM sample
    sequences),
    all implemented in Python which yields the Music package
    which yields the FIGGUS system.
* Consider psychophysic tests and make audiovisualizations with them.
* 
* Make music with the networks.
  - Revive the bot to scrappe FB.
  - Make music for Cristina, Chu, Antonio, etc etc
* Musify the Pedro Epistle.
  - Portuguese and Toki Pona (and english translation)
* Make a piece using RGB in (100,010,001,110,011,101,000,111)
as the sequence/scale with which to follow the pitches or whatever
parameter of the music or the voices.
use also (.5.50, .50.5, 0.5.5, .5.5.5)
and (1.50, .510,  10.5,.501,  01.5, 0.51)
are actually the ones that deviate the most
from uncollored things (black and white).
  - Use speech and subtitles to explain the
  proposal, the techniques: REM therapy and influence in cognition
  of change ringuing and reproducing REM when awake,
  arbitrary fidelity, enabling new gadgets an assuring
  that the sound is what we intend it to be.

* Make music for people (people suite?):
  - Chu e Cristina
  - Vilson, Ric, Gilson
  - Mae, Thata, Marina, Flavinha, Milena, Nadia, Gabi, Luciana, Bjork, Pri, Leticia, Debora, Laura, Ana Paula, Trindade, Laila, Fabs, Rita,
    Marilia, Tara, Karen Jolavescu, fabib, laura moraes, Maju, Karla, 
  - Pai, Israel, pastel, Rebecchi, Vini, Vanazzi, Lucas, Caleb, Silverio, Tiru, Daniel, Fred, Joca, Hugo, Tau, T, 

* Challenge in the social networks (FB, email, twitter):
  - 7 days to make an audiovisual album with 7 pieces

* Make a tutorial piece on MASS:
  - Use speech and singing to:
    * expose that the fourth section is relatively independent from the other two.
    * explain what MASS is, how it works and what we are able to do
      with it.
* Transitions:
  - Make linear, exponential and power-law transitions with various
    values of alpha
  - For freq, amp, ft, fv, fm, dB, nu, etc.
  - use espeak to describe transitions.
* Piece for numpy community:
  - uses the names of methods and modules input by function or startup
  - sings with ecantorix after espeak exhibitionism
  - uses random distributions and equations (e.g. polinomials)
  for sonic atributtes following Steven's and Weber-Fechner laws
  - as about the possibility of integratin mass or music into scipy
    (scikit?)
  - start another thread about numpy's documentation and how to derive
  the HTML files e.g. using doxigen.
  - put music and mass as python packages
* Testing the limits of a code for bugs is a source of musical creativity
because one often achieves unexpected sounds, both because of bugs,
and because of the limits employed.

##### 0 - Intro
# brown noise fades in.
# It oscilates L-R is cycles of 6s
# 3s-3s
# each compass (6 4) = six quarter notes of 1s each,
# beat = 3s

##### 1 - Presentation of the material
# sine or saw enters, very blended with the brown noise,
# a little lower on the right
# cycle is 1 compass.
# another voice enters, higher,
# with a cycle of three beats,
# which implies a cycle of 6 beats = three compass.

# Make three compass in 0-Intro when first voice enters,
# or play with cycles of 2 and 3 compass

##### 2 - Development
# harmonies are developed by many notes at the same time,
# and that don't oscilate as much as the brown noise and voices.

#### 3 - Development
# morph the brown noise.
# introduce slower and faster oscilations
# and static voices.
# Melodies and harmonies of voices and noises,
# imitations, hichups.

#### 4 - Recaptulation
# Make the scene stable again, as a soundscape
# Sounds and structures are changed, but they comunicate
# the same overall aspect.

#### 5 - Coda
# In some cycles a voice or noise is missing.
# Sounds get rare and the music ends.
# Maybe finish with a note + noise chord.

  
    





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
* position figures (FINAL)
* see if codes.pdf is not dropping out of the margin
* figgus package is very preliminary. Its principles are incorporated into music. It is interesting because:
  - It does use MASS but does not require numpy to render sonic arrays and write WAV files
  - Implements a whole EP album.
  - Inherits the original FIGGUS concepts (articles)
  - Is a step betwen original FIGGUS and the music package
* Mention that this work was called music in digital audio: psychophysic description and toolbox
* Cite more reference works that I've visited (from CCRMA, UPF, Brazil, England, Germany, IRCAM, etc)
* Very easy to inspect and assure the sound is what you expect it to be, in terms of the most used variables in physichophysics.
* Add about the functions.py!
* Permutations are also paths in the sonic state:
  - Each line of a peal in change ringuing is a path and a permutation
  - A permutation is sequential or cyclic notation is a path
  - Music makes peals and permutation groups and sets
  - Synths of Mass make symmetric scales within the octaves and 10 decibels
  - Modo intervalar (Vanazzi): cada nota tem uma nota associada.
  Function receives any melody: outputs upper or lower voice given
  the intervalar mode.
  - Distribution of harmonics is the sound: from lowest to highest components: df = fs/N. All harmonics of f = fs/N.
  - Use equal loudness contours (iso..),
  - implement Steven's loudness
  - Relate Steven's to the Weber-Fechner: power-law to exponential.
  - 
- visit wavepot

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
