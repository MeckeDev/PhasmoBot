from pynput import keyboard
import random

cfg_ordner = "D:\\SteamLibrary\\steamapps\\common\\Counter-Strike Global Offensive\\csgo\\cfg"


def neues_set(change):

    if change == "crosshair":

        # ################################ #
        # ##### Fadenkreuz erstellen ##### #
        # ################################ #

        alpha = random.randint(50, 255)
        thickness = random.uniform(0, 100)
        size = random.randint(0, 100)
        gap = random.randint(-100, 100)
        gap_fixed = random.randint(-100, 100)
        outline = random.randint(0, 3)
        style = random.randint(0, 5)

        farbe_rot = random.randint(0, 255)
        farbe_gruen = random.randint(0, 255)
        farbe_blau = random.randint(0, 255)

        dot = random.randint(0, 1)

        result = f'cl_crosshairalpha "{alpha}";' \
                 f'cl_crosshaircolor_r "{farbe_rot}";' \
                 f'cl_crosshaircolor_g "{farbe_gruen}";' \
                 f'cl_crosshaircolor_b "{farbe_blau}";' \
                 f'cl_crosshairdot "{dot}";' \
                 f'cl_crosshairgap "{gap}";' \
                 f'cl_crosshairsize "{size}";' \
                 f'cl_crosshairstyle "{style}";' \
                 f'cl_crosshairusealpha "1";' \
                 f'cl_crosshairthickness "{thickness}";' \
                 f'cl_fixedcrosshairgap "{gap_fixed}";' \
                 f'cl_crosshair_outlinethickness "{outline}";' \
                 f'cl_crosshair_drawoutline "1"'

    elif change == "viewmodel":

        # ############################### #
        # ##### Viewmodel erstellen ##### #
        # ############################### #

        shift_left = random.uniform(0, 2)    # wie stark das Model nach links geht beim schießen
        shift_right = random.uniform(0, 2)   # wie stark das Model nach rechts geht beim schießen
        fov = random.uniform(54, 68)         # wie viel man von der Waffe sehen kann
        righthand = random.randint(0, 1)     # Waffe in der linken oder der rechten Hand
        off_x = random.uniform(-2, 2)        # position der Waffe auf X-Achse
        off_y = random.uniform(-2, 2)        # position der Waffe auf Y-Achse
        off_z = random.uniform(-2, 2)        # position der Waffe auf Z-Achse
        bob_lower = random.randint(5, 30)    # wie weit das Model runtergeht beim rennen
        bob_lat = random.uniform(0, 2)       # wie stark das Model von Links nach Rechts wackelt
        bob_vert = random.uniform(0, 2)      # wie stark das Model von Oben nach Unten wackelt
        bob_cycle = random.uniform(0, 2)     # im Matchmaking automatisch 0.98 ( wie oft/schnell das model wackelt )

        result = f'cl_viewmodel_shift_left_amt "{shift_left}";' \
                 f'cl_viewmodel_shift_right_amt "{shift_right}";' \
                 f'viewmodel_fov "{fov}";' \
                 f'cl_righthand "{righthand}";' \
                 f'viewmodel_offset_x "{off_x}";' \
                 f'viewmodel_offset_y "{off_y}";' \
                 f'viewmodel_offset_z "{off_z}";' \
                 f'cl_bob_lower_amt "{bob_lower}";' \
                 f'cl_bobamt_lat "{bob_lat}";' \
                 f'cl_bobamt_vert "{bob_vert}";' \
                 f'cl_bobcycle "{bob_cycle}"'

    else:
        result = ""

    with open(f"{cfg_ordner}\\fadenkreuz.cfg", "w+") as f:
        f.write(result)

    return result
