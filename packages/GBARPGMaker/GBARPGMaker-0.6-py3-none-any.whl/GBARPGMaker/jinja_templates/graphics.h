#ifndef GRAPHICS_H
#define GRAPHICS_H

void moveScreen();

void forceMoveScreen(int screenx, int screeny);

{% for map_name in maps.keys() %}
void loadMap{{ map_name }}();
{% endfor -%}

u16 spriteAttrs[128][3];
int spriteRealSizes[128][2];

{%- for sprite_graphic_name in sprite_graphics.keys() %}
void loadSpriteGraphic{{ sprite_graphic_name }}();

void unloadSpriteGraphic{{ sprite_graphic_name }}();
{% endfor %}

void clearSpriteGraphics();

void updateSpriteAttr0(int spriteIndex);
void updateSpriteAttr1(int spriteIndex);
void updateSpriteAttr2(int spriteIndex);

void setSpriteX(int spriteIndex, int x);

void setSpriteY(int spriteIndex, int y);

int getSpriteX(int spriteIndex);

int getSpriteY(int spriteIndex);

void setSpriteDisable(int spriteIndex);

void setSpriteEnable(int spriteIndex);

void setSpritePriority(int spriteIndex, int p);

void setSpriteShowOnMap(int spriteIndex, bool show);

void moveSpriteOnMap(int spriteIndex, int x, int y);

{% for sprite_graphic_name in sprite_graphics.keys() %}
void setSpriteGraphics{{ sprite_graphic_name }}(int spriteIndex);
void setSpriteGraphicsFrame{{ sprite_graphic_name }}(int spriteIndex, int frameIndex);
{% endfor %}

int spriteCheckForSpecials(int spriteIndex, int spritex, int spritey);

int spriteCheckForFirstSpecial(int spriteIndex, int spritex, int spritey);

bool checkSpriteCollision(int spriteIndex1, int sprite1x, int sprite1y, int spriteIndex2, int sprite2x, int sprite2y);

void setHeroSpecialActions(void (*special_Actions_[])(void), int specialActionCount_);

void updateScreen();

void initHero(int* hero_x_pointer_, int* hero_y_pointer_, int hero_sprite_index_);

void printText(char* text);

void initText(char font[][8]);

void initGraphics();

#endif
