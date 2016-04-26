# emojicons

[![PyPI version](https://badge.fury.io/py/emojicons.svg)](https://pypi.python.org/pypi/emojicons/)
[![PyPI downloads](https://img.shields.io/pypi/dm/emojicons.svg?maxAge=2592000)](https://pypi.python.org/pypi/emojicons/)
[![Build Status](https://travis-ci.org/ruizink/emojicons.svg?branch=master)](https://travis-ci.org/ruizink/emojicons)

A very small python script that exposes a CLI and consumes http://emojicons.com/

## Available commands

### Online queries

#### Random

```
$ emoji random
  ID  Title                                           Emoji
----  ----------------------------------------------  -------------------------
 208  asian gang                                      (-(-(- -)-)-)
  99  street fight                                    Ｏ( ｀_´)乂(｀_´ )Ｏ
 409  Successful Thesis Defense                       ೖ(⑅σ̑ᴗσ̑)ೖ
 205  bunny ears                                      (”)(”)
 107  pigs need love too                              (｡･ω･｡)ﾉ♡
 254  pew pew                                         (　-_･)σ - - - - - - - - ･
 283  Tina Fey writing the last episode of '30 Rock'  ໒(⊙ᴗ⊙)७✎▤
 387  Winnie the Pooh                                 ʕ •́؈•̀)
 266  Rudolph the Red Nosed Reindeer                  3:*)
 270  So happy right now                              (●⌃ٹ⌃)
 361  perplexed                                       ( ⧉ ⦣ ⧉ )
 152  bowling cat                                     ◎ヽ(^･ω･^=)~
  52  sleepy                                          (-, - )…zzzZZZ
  96  flipping dude over                              (╯°Д°）╯︵ /(.□ . \)
```

#### Hall of fame

```
$ emoji hof
  ID  Title                Emoji
----  -------------------  --------------
  12  flipping tables      (╯°□°)╯︵ ┻━┻
   1  shrug                ¯\_(ツ)_/¯
  39  look of disapproval  ಠ_ಠ
   5  happy hands up       ლ(╹◡╹ლ)
  24  koala bear           ʕ •ᴥ•ʔ
   4  Nyan Cat             ~=[,,_,,]:3
 137  headphones           d-_-b
 212  O Hai                (●°u°●) 」
 220  kawaii shrug         ╮ (. ❛ ᴗ ❛.) ╭
```

#### Popular

```
$ emoji popular
  ID  Title                Emoji
----  -------------------  ------------------------
  71  sleepy flower girl   (◡ ‿ ◡ ✿)
  12  flipping tables      (╯°□°)╯︵ ┻━┻
 398  GIVE DIRETIDE        ༼ つ ◕_◕ ༽つ GIVE DIRETIDE
  24  koala bear           ʕ •ᴥ•ʔ
  28  y u no               ლ(ಠ益ಠლ)
  39  look of disapproval  ಠ_ಠ
  43  smiling breasts      （^人^）
 141  eff you              ┌∩┐(◣_◢)┌∩┐
 361  perplexed            ( ⧉ ⦣ ⧉ )
   4  Nyan Cat             ~=[,,_,,]:3
  45  middle finger up     t(-.-t)
 159  sloth                (⊙ω⊙)
   1  shrug                ¯\_(ツ)_/¯
   3  I dunno LOL          ¯\(º_o)/¯
```

#### Custom search

```
$ emoji search table
  ID  Title                  Emoji
----  ---------------------  -----------------------
  12  flipping tables        (╯°□°)╯︵ ┻━┻
  30  pudgy table flipping   (ノ ゜Д゜)ノ ︵ ┻━┻
  31  table flipping battle  (╯°□°)╯︵ ┻━┻ ︵ ╯(°□° ╯)
```

### Local operations

All local operations have an optional argument `--file` to override the default path `~/.emoji.json`

#### Save to file

```
$ emoji save 1
Emoji saved to '~/.emoji.json'
  ID  Title    Emoji
----  -------  ---------
   1  shrug    ¯\_(ツ)_/¯
```

#### List emojis from file

```
$ emoji list
  ID  Title        Emoji
----  -----------  ---------
   3  I dunno LOL  ¯\(º_o)/¯
   1  shrug        ¯\_(ツ)_/¯
```

#### Delete from file

```
$ emoji delete 284
Emoji with id '284' deleted from '~/.emoji.json'
```
