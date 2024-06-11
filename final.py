import pygame
import numpy as np
from copy import deepcopy

pygame.init()

pygame.display.set_caption("Hra Zivot")
SIRKA_DISLAY, VYSKA_DISLAY = 500, 500
OBRAZOVKA = pygame.display.set_mode((SIRKA_DISLAY, VYSKA_DISLAY))
STYL_TEXTU = pygame.font.Font(None, 32)
BARVA = (255,255,255)

class Aplikace_stranky:
    def __init__(self):
        self.stranka_1 = True
        self.stranka_2 = False
        self.stranka_random = False
        self.stranka_custom = False
        self.stranka_automata = False
        self.vyska_mrizky = ''
        self.sirka_mrizky = ''
        self.cislo_pravidla = '30'



class Text():
    def __init__(self, text, x, y, zglazivanie_textu = True, barva_textu = BARVA):
        self.text = text
        self.x = x
        self.y = y
        self.zglazivanie_textu = zglazivanie_textu
        self.barva_textu = barva_textu
        
    def zobrazit_text(self):
        poverhnost = STYL_TEXTU.render(self.text, self.zglazivanie_textu, self.barva_textu)
        OBRAZOVKA.blit(poverhnost, (self.x, self.y)) # копирует содержимое одной поверхности на другую. 
        
class Box_vstup():
    def __init__(self, x, y, delka_boxu = 100, vyska_boxu = 60, otstup_textu_po_x = 18, otstup_textu_po_y = 18, tloustka_hranic_boxu = 2, barva = (255,255,255), vyplnit =False): 
        self.x = x
        self.y = y
        self.delka_boxu = delka_boxu
        self.vyska_boxu = vyska_boxu
        self.box = pygame.Rect( x, y, delka_boxu, vyska_boxu)
        self.otstup_textu_po_x = otstup_textu_po_x
        self.otstup_textu_po_y = otstup_textu_po_y
        self.tloustka_hranic_boxu = tloustka_hranic_boxu
        self.text_v_boxu = ''
        self.aktiven = False
        self.aktivene_pole = (92,169,194) #(37, 150, 190)
        self.neaktivni_pole = barva
        self.barva = barva
        self.vyplnit = vyplnit
    
    def zobrazit_box(self):
        if self.vyplnit:
            pygame.draw.rect(OBRAZOVKA, self.neaktivni_pole, self.box)
        pygame.draw.rect(OBRAZOVKA, self.barva, self.box, self.tloustka_hranic_boxu)

            

    def zmacknuti(self, event): 
        if self.box.collidepoint(event.pos):
            self.aktiven = not self.aktiven
            if self.aktiven:
                self.barva = self.aktivene_pole
            else: self.barva = self.neaktivni_pole
            
    def uzivatelky_vstup(self, event):
            if self.aktiven:
                if event.key == pygame.K_BACKSPACE:
                    self.text_v_boxu = self.text_v_boxu[:-1]
                
                else:
                    self.text_v_boxu += event.unicode
                    
    def zobrazit_input_data(self):
        input_text = Text(self.text_v_boxu, self.x + self.otstup_textu_po_x, self.y + self.otstup_textu_po_y)
        input_text.zobrazit_text()
            

class Tlacitko():
    def __init__(self, x, y, obrazek, vyska_tlacitka, sirka_tlacitka):
        self.vyska_tlacitka = vyska_tlacitka
        self.sirka_tlacitka = sirka_tlacitka
        self.obrazek = pygame.transform.scale(obrazek, (self.vyska_tlacitka, self.sirka_tlacitka))
        self.box_umisteni_tlacitka = self.obrazek.get_rect(topleft = (x,y))
        self.x = x
        self.y = y
        self.pause = False
        
    def zobrazit_tlacitko(self):
        OBRAZOVKA.blit(self.obrazek, (self.x, self.y))

    def prechod_mezi_stranky(self, event, stavy_aplikace, z_stranky, do_stranky):
        if self.box_umisteni_tlacitka.collidepoint(event.pos):
            tekusi_stav = getattr(stavy_aplikace, z_stranky)
            nasledujici_stav = getattr(stavy_aplikace, do_stranky)
            setattr(stavy_aplikace, z_stranky, not tekusi_stav)
            setattr(stavy_aplikace, do_stranky, not nasledujici_stav)
        return stavy_aplikace
    
    def pause_play(self, obrazek_pause, obrazek_play, event):
        if self.box_umisteni_tlacitka.collidepoint(event.pos):
            self.pause = not self.pause
            novy_obrazek = obrazek_play if self.pause else obrazek_pause
            self.obrazek = pygame.transform.scale(novy_obrazek, (self.vyska_tlacitka, self.sirka_tlacitka))
            
    def zmenit_cislo_pravisla(self, event, box, stavy_aplikace):
        if self.box_umisteni_tlacitka.collidepoint(event.pos):
            stavy_aplikace.cislo_pravidla = box.text_v_boxu
        return stavy_aplikace



def obrazovka_1(vyska_box, sirka_box, next_tlacitko, stavy_aplikace):    
    title = Text("Zapocet python", 170, 50)
    title.zobrazit_text()
    
    vyska_box.zobrazit_box()
    text_vlevo_vyska = Text("Vyska mrizky", 100,168) 
    text_vlevo_vyska.zobrazit_text()

    sirka_box.zobrazit_box()
    text_vlevo_sirka = Text("Sirka mrizky", 100, 268) 
    text_vlevo_sirka.zobrazit_text()
        
    next_tlacitko.zobrazit_tlacitko()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            vyska_box.zmacknuti(event)
            sirka_box.zmacknuti(event)
            setattr(stavy_aplikace, 'vyska_mrizky', vyska_box.text_v_boxu)
            setattr(stavy_aplikace, 'sirka_mrizky', sirka_box.text_v_boxu)
            stavy_aplikace = next_tlacitko.prechod_mezi_stranky(event, stavy_aplikace, 'stranka_1', 'stranka_2')
                
        elif event.type == pygame.KEYDOWN:
            vyska_box.uzivatelky_vstup(event)
            sirka_box.uzivatelky_vstup(event)
            
    vyska_box.zobrazit_input_data()
    sirka_box.zobrazit_input_data()
    
    return stavy_aplikace
    
    
def obrazovka_2(back_tlacitko, random_tlacitko, custom_tlacitko, stavy_aplikace, automata_tlacitko):
    back_tlacitko.zobrazit_tlacitko()
    
    text_rand = Text("Nahodna mrizka", 30, 125) 
    text_rand.zobrazit_text()
    random_tlacitko.zobrazit_tlacitko()
    
    text_cust = Text('Custom mrizka', 30, 300) 
    text_cust.zobrazit_text()
    custom_tlacitko.zobrazit_tlacitko()
    
    text_aut_1 = Text("Cellular", 290, 200) 
    text_aut_2 = Text("automata", 285, 240) 
    text_aut_1.zobrazit_text()
    text_aut_2.zobrazit_text()
    automata_tlacitko.zobrazit_tlacitko() 
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            stavy_aplikace = back_tlacitko.prechod_mezi_stranky(event, stavy_aplikace, 'stranka_2', 'stranka_1')
            stavy_aplikace = custom_tlacitko.prechod_mezi_stranky(event, stavy_aplikace, 'stranka_2', 'stranka_custom')
            stavy_aplikace = random_tlacitko.prechod_mezi_stranky(event, stavy_aplikace, 'stranka_2', 'stranka_random')
            stavy_aplikace = automata_tlacitko.prechod_mezi_stranky(event, stavy_aplikace, 'stranka_2', 'stranka_automata')
    return stavy_aplikace


def custom_vytvoreni(back_tlacitko, stavy_aplikace):    
    text = Text("Bude pridano Pozdeji", 100, 200)
    text.zobrazit_text()
    back_tlacitko.zobrazit_tlacitko()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            stavy_aplikace = back_tlacitko.prechod_mezi_stranky(event, stavy_aplikace, 'stranka_custom', 'stranka_2')
            
    return stavy_aplikace



def vytvorit_nahodnou_mrizku(stavy_aplikace):
    pole = np.array([[np.random.randint(0,2) for i in range (int(stavy_aplikace.sirka_mrizky))] for j in range(int(stavy_aplikace.vyska_mrizky))], dtype = int)
    return pole

def osud_bunky(hodnota_bunky, pocet_sousedu):
    if hodnota_bunky == 0 and pocet_sousedu == 3:
        hodnota_bunky = 1
    
    if hodnota_bunky == 1 and (pocet_sousedu < 2 or pocet_sousedu > 3):
        hodnota_bunky = 0
    
    return hodnota_bunky

 
def vytvorit_povrh_mrizky(pole):
    radky, sloupce = pole.shape

    rgb_matice = np.zeros((radky, sloupce, 3), dtype = np.uint8)
    rgb_matice[pole==1] = [0, 0, 0]
    rgb_matice[pole==0] = [255, 255, 255]
    povrh_matice = pygame.Surface((radky, sloupce))
    pygame.surfarray.blit_array(povrh_matice, rgb_matice) # преобразования массива в поверхность
    
    return povrh_matice
        
def vykreslit_preskalovanou_mrizku(pole):
    povrh_matice = vytvorit_povrh_mrizky(pole)
    preskal_povrh = pygame.transform.scale(povrh_matice, (SIRKA_DISLAY, VYSKA_DISLAY))
    OBRAZOVKA.blit(preskal_povrh, (0,0))
    
def random_zivot(stavy_aplikace, back_tlacitko, pole, pause_tlacitko, obrazek_play, obrazek_pause):
    vyska = int(stavy_aplikace.vyska_mrizky)
    sirka = int(stavy_aplikace.sirka_mrizky)
    
    while stavy_aplikace.stranka_random == True and pause_tlacitko.pause == False:
        novy_stav_pole = deepcopy(pole)
        for i in range(vyska):
            for j in range(sirka):
                pocet_zs = (
                    pole[(i-1) % vyska, (j-1) % sirka] + pole[(i-1) % vyska, j % sirka] + pole[(i-1) % vyska, (j+1) % sirka] +
                    pole[i % vyska, (j-1) % sirka] + pole[i % vyska, (j+1) % sirka] +
                    pole[(i+1) % vyska, (j-1) % sirka] + pole[(i+1) % vyska, j % sirka] + pole[(i+1) % vyska, (j+1) % sirka]
                )
                nova_hodnota_bunky = osud_bunky(pole[i, j], pocet_zs)
                novy_stav_pole[i, j] = nova_hodnota_bunky
        pole = deepcopy(novy_stav_pole) 

        vykreslit_preskalovanou_mrizku(pole)
        back_tlacitko.zobrazit_tlacitko()
        pause_tlacitko.zobrazit_tlacitko()
        pygame.display.update()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                stavy_aplikace = back_tlacitko.prechod_mezi_stranky(event, stavy_aplikace, 'stranka_random', 'stranka_2')
                pause_tlacitko.pause_play(obrazek_pause, obrazek_play, event)
                pause_tlacitko.zobrazit_tlacitko()
                
                
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            stavy_aplikace = back_tlacitko.prechod_mezi_stranky(event, stavy_aplikace, 'stranka_random', 'stranka_2')
            pause_tlacitko.pause_play(obrazek_pause, obrazek_play, event)      
    return stavy_aplikace, pole



def stranka_automata(stavy_aplikace, back_tlacitko, podtvrdit_tlacitko, pravidlo_box):
    pravidlo = int(stavy_aplikace.cislo_pravidla)
    vyska = int(stavy_aplikace.vyska_mrizky)
    sirka = int(stavy_aplikace.sirka_mrizky) 
    pole = hra(pravidlo, vyska, sirka)
    pole = np.transpose(pole)
    
    vykreslit_preskalovanou_mrizku(pole)
    back_tlacitko.zobrazit_tlacitko()
    podtvrdit_tlacitko.zobrazit_tlacitko()
    pravidlo_box.zobrazit_box()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            stavy_aplikace = back_tlacitko.prechod_mezi_stranky(event, stavy_aplikace, 'stranka_automata', 'stranka_2')
            pravidlo_box.zmacknuti(event)
            stavy_aplikace = podtvrdit_tlacitko.zmenit_cislo_pravisla(event, pravidlo_box, stavy_aplikace)
        elif event.type == pygame.KEYDOWN:
            pravidlo_box.uzivatelky_vstup(event)
            
    pravidlo_box.zobrazit_input_data()
    pygame.display.update()

    return stavy_aplikace

def hra(cislo_pravidla, vyska_pole, sirka_pole):
    pravidlo = f'{cislo_pravidla:08b}'
    pravidlo = [int(cislo) for cislo in pravidlo]

    pole = np.zeros((vyska_pole, sirka_pole), dtype = int)   
    pocatecni_bunka = int(np.floor(sirka_pole/2)) # ceil
    pole[0][pocatecni_bunka] = 1
    
    for i in range(0,  vyska_pole-1):
        for j in range(1, sirka_pole - 1):
            bin_cislo = ''.join(str(cislo) for cislo in pole[i, j-1:j+2])
            idx = int(bin_cislo, 2)
            pole[i+1, j] = pravidlo[-(idx+1)]
    return pole
   
def main():
    stavy_aplikace = Aplikace_stranky()
    #1
    vyska_box = Box_vstup(300,150)
    sirka_box = Box_vstup(300,250)
    
    obrazek_next_tlacitko = pygame.image.load('src/next.png').convert_alpha()
    next_tlacitko = Tlacitko(400, 400, obrazek_next_tlacitko, 60, 60)
    
    #2
    obrazek_back = pygame.transform.rotate(obrazek_next_tlacitko, 180)
    back_tlacitko = Tlacitko(20, 20, obrazek_back, 60, 60)

    obrazek_random = pygame.image.load('src/surprise-box.png')
    random_tlacitko = Tlacitko(90, 165, obrazek_random, 70, 70) 
    
    obrazek_custom = pygame.image.load('src/customize.png')
    custom_tlacitko = Tlacitko(90, 350, obrazek_custom, 65, 65) #90 x
    
    obrazek_automata = pygame.image.load('src/automat.png')
    automata_tlacitko = Tlacitko(300, 285, obrazek_automata, 85, 70) # 300 285 
    
    # rand
    obrazek_pause = pygame.image.load('src/pause.png')
    obrazek_play = pygame.image.load('src/play.png')
    pause_tlacitko = Tlacitko(420, 20, obrazek_pause, 55, 55)
    
    # aut
    obrazek_confirm = pygame.image.load('src/confirm.png')
    podtvrdit_tlacitko = Tlacitko(420, 100, obrazek_confirm, 55,55)
    pravidlo_box = Box_vstup(390, 20, delka_boxu = 85, vyska_boxu = 60, barva=(0, 0, 0), vyplnit= True) # (92,169,194)

    while True:
        while stavy_aplikace.stranka_random != True and stavy_aplikace.stranka_automata != True :#or stavy_aplikace.stranka_automata != True    
            if stavy_aplikace.stranka_1:        
                OBRAZOVKA.fill((10,25,40))
                stavy_aplikace = obrazovka_1(vyska_box, sirka_box, next_tlacitko, stavy_aplikace)
                pygame.display.update()
            elif stavy_aplikace.stranka_2:
                OBRAZOVKA.fill((10,25,40))
                stavy_aplikace = obrazovka_2(back_tlacitko, random_tlacitko, custom_tlacitko, stavy_aplikace, automata_tlacitko)
                pygame.display.update()
            elif stavy_aplikace.stranka_custom:
                OBRAZOVKA.fill((10,25,40))
                stavy_aplikace = custom_vytvoreni(back_tlacitko, stavy_aplikace)
                pygame.display.update()    
            
        pole = vytvorit_nahodnou_mrizku(stavy_aplikace)
        pause_tlacitko.pause = False
        while stavy_aplikace.stranka_random == True:
            stavy_aplikace, pole = random_zivot(stavy_aplikace, back_tlacitko, pole, pause_tlacitko, obrazek_play, obrazek_pause) #0, 90 az 500 500
            pygame.display.update()
           
        while stavy_aplikace.stranka_automata == True:
            stavy_aplikace = stranka_automata(stavy_aplikace, back_tlacitko, podtvrdit_tlacitko, pravidlo_box)



main()
# pozice_mysi = pygame.mouse.get_pos()
# print(pozice_mysi)
