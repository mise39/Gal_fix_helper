# 本軟體是方便大家修正視覺小說的動畫錯誤 (主要是給Steam Deck用的)
60% AI構成(20% ChatGPT + 40% Grok)和40%人工反覆修正。  
無需任何Python額外插件。
* 已知缺陷: 不支援Proton7或更舊版本啟動的遊戲。
## 使用方法:
1. 先下載 Gal_fix_helper.py 和 Gal_fix_helper.sh  
2. 下載 [官方](https://github.com/b-fission/vn_winestuff/)
  或 [備份源](https://drive.google.com/file/d/1DauMsfuTvxjLMu3B_8W5p_cd2foIkwGl/view?usp=drive_link) 的vn_winestuff
3. 把下載的解壓縮在同一個目錄(即是 Gal_fix_helper.py ,  Gal_fix_helper.sh , vn_winestuff-main資料夾 在同一目錄)
4. 開啟Konsole指令台。  
5. 輸入指令  
```
chmox +x /你的檔案位置/Gal_fix_helper.sh
```
6. 把這個".sh"加入到非Steam遊戲，然後再執行。

# *關於Chmod not found的解決方法
請先konsole輸入
```
passwd
```
設定密碼 然後再輸入
```
sudo pacman -Sy coreutils
```
Chmod 指令就不會報錯

1.2版本增加字體修正指令，字體教學如下: 

[![IMAGE ALT TEXT](https://i9.ytimg.com/vi_webp/FPxgC8YdCX4/mqdefault.webp?v=687538aa&sqp=CLzx1MMG&rs=AOn4CLCYxMACPk1Dw0rDkMJnQ4zJ9OfGQQ)](https://www.youtube.com/watch?v=FPxgC8YdCX4) 


[Fonts](https://drive.google.com/file/d/1b1-M2UWKXJ7pBGmbaP6RcGN5zXMTgbPo/view?usp=drive_link)
字體的資料夾fonts放在Gal_fix_helper同一目錄下，文件夾名不能改，但字體可以放你喜歡的字體檔(有可能沒效果)，
也可以用我準備的字體檔，點擊修正字體鍵就會更新.fonts-wine.conf和路徑指令。
* * *

# ENGLISH
# This software is designed to help fix animation errors in visual novels (mainly for Steam Deck).
60% AI-generated (20% ChatGPT + 40% Grok) and 40% manually refined.
No additional Python plugins required.  
* Known issue: Does not support games launched with Proton 7 or older versions.

## Usage Instructions:
1. Download Gal_fix_helper.py and Gal_fix_helper.sh.  
2. Download vn_winestuff from the [official source](https://github.com/b-fission/vn_winestuff/)
  or [the backup source](https://drive.google.com/file/d/1DauMsfuTvxjLMu3B_8W5p_cd2foIkwGl/view?usp=drive_link).
3. Extract the downloaded files to the same directory (i.e., Gal_fix_helper.py, Gal_fix_helper.sh, and the vn_winestuff-main folder should be in the same directory).  
4. Open the Konsole terminal.  
5. Enter the following command:
```
chmod +x /your/file/path/Gal_fix_helper.sh
```
6. Add the .sh file to non-Steam games, then execute it.

# *Solution for "Chmod not found" error
In Konsole, first enter:  
```
passwd
```
Set a password, then enter:  
```
sudo pacman -Sy coreutils
```
The chmod command should no longer report an error.

