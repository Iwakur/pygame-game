from dataclasses import dataclass
import pygame, pytmx, pyscroll
import os.path

from pygame.sprite import Sprite

from item import Item
PLAY_MUSIC = True

@dataclass
class Portal:
    from_map: str
    portal_point: str
    target_world: str
    spawn_point: str


@dataclass
class Map:
    name: str
    obstacles: list[pygame.Rect]
    portals: list[Portal]
    music: bool
    tmx_data: pytmx.TiledMap = None
    group: pyscroll.PyscrollGroup = None
    loaded: bool = False


def get_objects_by_type(tmx_data, type):
    return [x for x in tmx_data.objects if hasattr(x.type, "lower") and x.type.lower() == type.lower()]


class MapManager:

    def __init__(self, screen, player):
        self.maps = dict()  # "house" -> Map("house", obstacles, group
        self.current_map = ""

        self.screen = screen
        self.player = player

        # self.register_map("nature", portals=[
        #     # Portal(from_map="nature", portal_point="enter-house", target_world="mega-house", spawn_point="spawn"),
        #     # Portal(from_map="nature", portal_point="enter-tiny-house", target_world="tiny-house", spawn_point="spawn")
        # ])

        # Parcourir les dossiers dans le répertoire ../assets/maps/ et charger les fichiers.tmx
        root = "../assets/maps/"
        print("Looking for maps in ", root)
        for dirname in os.listdir(root):

            # Vérifier si c'est une dossier
            map_file_name = f"{root}{dirname}/{dirname}.tmx"

            if os.path.isdir(root + dirname) and os.path.isfile(map_file_name):
                self.register_map(dirname)

        # Validate that all portals point to a valid map
        # for map in self.maps.values():
        #     print("•", map.name)
        #     for portal in map.portals:
        #         print("    >", portal.from_map, portal.portal_point, portal.target_world)
        #         if portal.from_map not in self.maps:
        #             print("Invalid portal from map: ", portal.from_map)
        #         if portal.target_world not in self.maps:
        #             print("Invalid portal to map: ", portal.target_world)

        # self.register_map("tiny-house")
        # self.register_map("mega-house")
        #
        self.set_current_map("main")
        # self.set_current_map("cepes_tir_gymnase")

    # Set the current map and register it if it doesn't exist yet
    def set_current_map(self, name, spawn_point="main"):
        print("************", self, name)
        if name not in self.maps:
            print("Map not found: ", name)
            return None
        else:
            # lazy load the map
            print("Lazy loading map: ", name)

            if not self.maps[name].loaded:
                self.load_map(name)

            self.current_map = name
            print("Spawning to:", spawn_point)
            self.spawn(spawn_point)

            if self.get_map().music:  # load music from thu current map's folder
                pygame.mixer.music.load(self.get_map().music)
            else:
                print("No music")

            if PLAY_MUSIC:
                pygame.mixer.music.play(-1)

    def debug(self, map):
        for portal in self.maps[map].portals:
            portal_point = self.get_object(portal.portal_point)
            print("Portal Point: ", portal_point,
                  pygame.Rect(portal_point.x, portal_point.y, portal_point.width, portal_point.height))

    def check_collisions(self):

        # Portals
        for portal in self.get_map().portals:

            if portal.from_map == self.current_map:
                p = self.get_object(portal.portal_point)
                rect = pygame.Rect(p.x, p.y, p.width, p.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.set_current_map(portal.target_world, copy_portal.spawn_point)

                    # self.spawn(copy_portal.spawn_point)
                # else:
                # print("No Portal")

        # Collision
        for sprite in self.get_group().sprites():
            if hasattr(sprite, "feet") and sprite.feet.collidelist(self.get_obstacles()) > -1:
                sprite.move_back()

    def spawn(self, name):

        """Spawn the player at the given point"""

        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

        name = self.get_map().name

        # play music ?

    # lazy load the map
    def load_map(self, name):

        # Auto-register map if it doesn't exist'
        if name not in self.maps:
            self.register_map(name)

        map = self.maps[name]

        # Charger la carte
        filename = "../assets/maps/" + name + "/" + name + ".tmx"
        print("Loading map from: ", name)

        tmx_data = pytmx.util_pygame.load_pygame(filename)
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 1
        map.tmx_data = tmx_data
        map.map_layer = map_layer

        portals = get_objects_by_type(tmx_data, "portal")
        print("Portals: ", portals)
        for p in portals:
            print("  • Portal: ", p.name, p.properties.get("spawn", "main"))

            if "map" in p.properties:
                print("  • Map: ", p.properties["map"])
                target_map = p.properties["map"]
            else:
                target_map = p.name

            map.portals.append(
                # Portal(from_map="nature", portal_point="enter-house", target_world="mega-house", spawn_point="spawn"),
                # check if portal has a map property
                Portal(from_map=name, portal_point=p.name, target_world=target_map, spawn_point=p.properties.get("spawn", "main"))
            )

        spawn_points = get_objects_by_type(tmx_data, "spawn")
        print("Spawns: ", spawn_points)

        # Définir les collisions
        obstacles = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                obstacles.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        map.obstacles = obstacles

        # Dessiner les différents calques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=7)
        group.add(self.player)
        map.group = group
        map.loaded = True

        # portals: list[Portal]

    def register_map(self, name):

        print("Registering map", name)

        filename = "../assets/maps/" + name + "/" + name + ".tmx"
        #tmx_data = pytmx.util_pygame.load_pygame(filename)

        # Créer l'objet map
        music = "../assets/maps/" + name + "/" + name + ".mp3"
        if not os.path.isfile(music):
            music = "../assets/maps/common/common.mp3"

        self.maps[name] = Map(name, [], [], music)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_obstacles(self):
        return self.get_map().obstacles

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def draw(self):

        # self.highlite_items()

        self.get_group().draw(self.screen)

        # for item in self.items:
        #     couleur_contour = (255, 255, 0)  # Jaune
        #     epaisseur_contour = 2  # Épaisseur du contour en pixels
        #
        #     v = self.get_group().view
        #
        #    pygame.draw.rect(, couleur_contour, item.rect, epaisseur_contour)

        self.get_group().center(self.player.rect.center)


    items=[]
    def highlite_items(self):

        for obj in self.get_map().tmx_data.objects:
            if obj.type == "item":

                # Check if there is file for this item
                f = "../assets/items/" + obj.name + ".png"
                if not os.path.isfile(f):
                    print("Item not found: ", obj.name)
                    continue

                # Simply draw items as Sprites
                surface = pygame.image.load(f).convert_alpha()
                sprite = Item(surface, obj.x, obj.y)
                self.items.append(sprite)
                self.get_group().add(sprite)

#                screen_rect = self.get_map().map_layer.map_rect
#                highlight_rect = pygame.Rect(obj.x , obj.y, obj.width, obj.height)
#                pygame.draw.rect(self.screen, (200, 200, 200), highlight_rect, 3)

    def update(self):
        self.get_group().update()
        self.check_collisions()

