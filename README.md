### 注意 Note: 
* 要求 Python 3.x  
   Python 3.x required
---
* 适用于tModLoader 0.11+  
   Applicable to tModLoader 0.11+
---
* **仅供mod制作者使用，由于许多mod非开源，拆包前请仔细阅读mod的Licence，尊重作者的劳动成果.** 
**Only for modders, cause many mods aren't open source, please check out their licenses before you extract the .tmod file, respect authors' labor.**


### 用法 Usage:
* extract `.tmod` file
  ```
    python launch.py mod1-path [mod2-path] ...
  ```
### TODO:
- [x] .tmod file extraction
- [ ] .tmod file localization
- [ ] performance optimization
- [ ] tModLoader previous version support

### Tips:
* .tmod data format  
see [TmodFile.cs](https://github.com/tModLoader/tModLoader/blob/master/patches/tModLoader/Terraria.ModLoader.Core/TmodFile.cs)

* image data format conversion  
png images are convert to .rawimg when packing .tmod file，see [ImageIO.cs](https://github.com/tModLoader/tModLoader/blob/c54a8fc44ef25f8ff96114c09e86632f320f4304/patches/tModLoader/Terraria.ModLoader.IO/ImageIO.cs)
