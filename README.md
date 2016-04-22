# emojicons
A very small python script that exposes a CLI and consumes http://emojicons.com/

## Available commands

### On-line queries

#### Random

```
$ emoji random
Title                                Emoji
-----------------------------------  -----------------
nothing to see here                  (̿▀̿ ̿Ĺ̯̿̿▀̿ ̿)̄
Beyoncé at Super Bowl Halftime Show  ♪~♪ ヽ໒(⌒o⌒)७ﾉ ♪~♪
pig who wishes to fly                (｀◔ ω ◔´)
Would you like some cake?            ( ・∀・)っ旦
you crazy                            (☞ﾟ∀ﾟ)☞
stop poking me                       (*・)σσσ(*゜Д゜*)
praying                              八(＾□＾*)
Boy Meets Girl                       웃❤유
gasp face                            (○口○ )
Bane                                 ⋋( 'Θ')⋌
one more thing                       (°ロ°)☝
I rest my case                       ┐( ˘_˘)┌
NSA Smiley                           ˙ ͜ʟ˙
face palm                            (－‸ლ)
```

#### Hall of fame

```
$ emoji hof
Title                Emoji
-------------------  --------------
flipping tables      (╯°□°)╯︵ ┻━┻
shrug                ¯\_(ツ)_/¯
look of disapproval  ಠ_ಠ
happy hands up       ლ(╹◡╹ლ)
koala bear           ʕ •ᴥ•ʔ
Nyan Cat             ~=[,,_,,]:3
headphones           d-_-b
O Hai                (●°u°●) 」
kawaii shrug         ╮ (. ❛ ᴗ ❛.) ╭
```

#### Popular

```
$ emoji popular
Title                Emoji
-------------------  ------------------------
sleepy flower girl   (◡ ‿ ◡ ✿)
flipping tables      (╯°□°)╯︵ ┻━┻
GIVE DIRETIDE        ༼ つ ◕_◕ ༽つ GIVE DIRETIDE
koala bear           ʕ •ᴥ•ʔ
y u no               ლ(ಠ益ಠლ)
look of disapproval  ಠ_ಠ
smiling breasts      （^人^）
eff you              ┌∩┐(◣_◢)┌∩┐
perplexed            ( ⧉ ⦣ ⧉ )
Nyan Cat             ~=[,,_,,]:3
middle finger up     t(-.-t)
sloth                (⊙ω⊙)
shrug                ¯\_(ツ)_/¯
I dunno LOL          ¯\(º_o)/¯
```

#### Custom search

```
$ emoji search table
Title                  Emoji
---------------------  -----------------------
flipping tables        (╯°□°)╯︵ ┻━┻
pudgy table flipping   (ノ ゜Д゜)ノ ︵ ┻━┻
table flipping battle  (╯°□°)╯︵ ┻━┻ ︵ ╯(°□° ╯)
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

#### List emojis form file

```
$ emoji list
  ID  Title        Emoji
----  -----------  ---------
   3  I dunno LOL  ¯\(º_o)/¯
   1  shrug        ¯\_(ツ)_/¯
```