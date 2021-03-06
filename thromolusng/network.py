# thromolusng - a game
# Copyright (C) 2009 Florian Mayer

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asynchia
import asynchia.ee

import itertools

enum = itertools.count()

TYPE_GAME = enum.next()
TYPE_TURN = enum.next()


class PackageCollector(asynchia.ee.CollectorQueue):
    def __init__(self, typemap, *args, **kwargs):
        asynchia.ee.CollectorQueue(self, 
            [asynchia.ee.StructCollector('B', self.pickedtype)]
            )
        self.args = args
        self.kwargs = kwargs
        self.typemap = typemap
    
    def pickedtype(self, coll):
        self.add_collector(self.typemap[coll.value](*args, **kwargs))


class GameCollector(asynchia.ee.CollectorQueue):
    def __init__(self, games):
        asynchia.ee.CollectorQueue(self,
            [asynchia.ee.StructCollector('B', self.pickedgame)]
        )
             
        self.game = None
        self.games = games
    
    def pickedgame(self, coll):
        self.game = self.games[coll.value]
        self.add_collector(PackageCollector(GAME_TYPEMAP, self.game))


class MainCollector(asynchia.ee.FactoryCollector):    
    def __init__(self, games):
        asynchia.ee.FactoryCollector.__init__(
            self,
            factory=lambda: PackageCollector(TOP_TYPEMAP, games)
        )
        self.games = games


class TurnCollector(asynchia.ee.StructCollector):
    def __init__(self, game):
        asynchia.ee.StructCollector('B' * 4)
        self.game = game
    
    def close(self):
        asynchia.ee.StructCollector.close()
        origin_x, origin_y, target_x, target_y = self.value
        self.game.turn((origin_x, origin_y), (target_x, target_y))
    
    
GAME_TYPEMAP = {
    TYPE_TURN: TurnCollector
}

TOP_TYPEMAP = {
    TYPE_GAME: GameCollector,
}
