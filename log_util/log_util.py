from hearthstone.enums import CardType, Zone, GameTag
from hslog import LogParser, packets
from hslog.export import EntityTreeExporter
import os
from entity.game_entity import GameEntity
from entity.hero_entity import HeroEntity
from entity.spell_entity import SpellEntity


class LogUtil:
    def __init__(self, log_path):
        self.log_path = log_path
        self.parser = LogParser()
        self.game = None
        # parse 完后可直接拿来用
        self.game_entity = None

    def read_log(self):
        with open(self.log_path, encoding='utf-8') as f:
            self.parser.read(f)
        self.parser.flush()
        # 最近一场战斗
        packet_tree = self.parser.games[-1]
        exporter = EntityTreeExporter(packet_tree, player_manager=self.parser.player_manager)
        ee = exporter.export()
        self.game = ee.game

    def parse_game(self) -> GameEntity:
        self.read_log()
        for e in self.game.entities:
            # 以下为游戏状态
            if e.type == CardType.GAME:
                self.game_entity = GameEntity(e)
                pass
            elif e.type == CardType.MINION:
                minion = HeroEntity(e)

                # print(e, e.tags, end='\n\n\n')
                self.game_entity.add_hero(minion)
                pass
            # 佣兵技能信息
            elif e.type == CardType.LETTUCE_ABILITY:
                # print(e, e.tags, end='\n\n\n')
                spell_entity = SpellEntity(e)
                if spell_entity.lettuce_ability_owner in self.game_entity.hero_entities.keys():
                    self.game_entity.hero_entities[spell_entity.lettuce_ability_owner].add_spell(spell_entity)
                pass
            # 对战技能记录
            elif e.type == CardType.SPELL:
                pass
            # print(e, e.tags, end='\n\n\n')
        return self.game_entity

    pass


if __name__ == '__main__':
    path = ["D:/", "Hearthstone", "Logs", "Power.log"]
    hs_log = LogUtil(path)
    game_entity = hs_log.parse_game()
    for i in game_entity.my_hero:
        print(i)

    for i in game_entity.enemy_hero:
        print(i)

    pass
