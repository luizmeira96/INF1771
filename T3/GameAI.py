#!/usr/bin/env python

"""GameAI.py: INF1771 GameAI File - Where Decisions are made."""
#############################################################
#Copyright 2020 Augusto Baffa
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#############################################################
__author__      = "Augusto Baffa"
__copyright__   = "Copyright 2020, Rio de janeiro, Brazil"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "abaffa@inf.puc-rio.br"
#############################################################

import random
from Map.Position import Position
from datetime import time

# <summary>
# Game AI Example
# </summary>
class GameAI():

    player = Position()
    state = "ready"
    dir = "north"
    score = 0
    energy = 0

     current_observations = {
        "blocked": False,
        "steps": False,
        "flash": False,
        "blueLight": False,
        "redLight": False,
        "greenLight": False,
        "breeze": False,
        "damage": False,
        "hit": False,
        "enemy_in_front": False
    }

    # <summary>
    # Refresh player status
    # </summary>
    # <param name="x">player position x</param>
    # <param name="y">player position y</param>
    # <param name="dir">player direction</param>
    # <param name="state">player state</param>
    # <param name="score">player score</param>
    # <param name="energy">player energy</param>
    def SetStatus(self, x, y, dir, state, score, energy):
    
        self.player.x = x
        self.player.y = y
        self.dir = dir.lower()

        self.state = state
        self.score = score
        self.energy = energy


    # <summary>
    # Get list of observable adjacent positions
    # </summary>
    # <returns>List of observable adjacent positions</returns>
    def GetObservableAdjacentPositions(self):
        ret = []

        ret.append(Position(self.player.x - 1, self.player.y))
        ret.append(Position(self.player.x + 1, self.player.y))
        ret.append(Position(self.player.x, self.player.y - 1))
        ret.append(Position(self.player.x, self.player.y + 1))

        return ret


    # <summary>
    # Get list of all adjacent positions (including diagonal)
    # </summary>
    # <returns>List of all adjacent positions (including diagonal)</returns>
    def GetAllAdjacentPositions(self):
    
        ret = []

        ret.Add(Position(self.player.x - 1, self.player.y - 1))
        ret.Add(Position(self.player.x, self.player.y - 1))
        ret.Add(Position(self.player.x + 1, self.player.y - 1))

        ret.Add(Position(self.player.x - 1, self.player.y))
        ret.Add(Position(self.player.x + 1, self.player.y))

        ret.Add(Position(self.player.x - 1, self.player.y + 1))
        ret.Add(Position(self.player.x, self.player.y + 1))
        ret.Add(Position(self.player.x + 1, self.player.y + 1))

        return ret
    

    # <summary>
    # Get next forward position
    # </summary>
    # <returns>next forward position</returns>
    def NextPosition(self):
    
        ret = None
        
        if self.dir == "north":
            ret = Position(self.player.x, self.player.y - 1)
                
        elif self.dir == "east":
                ret = Position(self.player.x + 1, self.player.y)
                
        elif self.dir == "south":
                ret = Position(self.player.x, self.player.y + 1)
                
        elif self.dir == "west":
                ret = Position(self.player.x - 1, self.player.y)

        return ret
    

    # <summary>
    # Player position
    # </summary>
    # <returns>player position</returns>
    def GetPlayerPosition(self):
        return self.player


    # <summary>
    # Set player position
    # </summary>
    # <param name="x">x position</param>
    # <param name="y">y position</param>
    def SetPlayerPosition(self, x, y):
        self.player.x = x
        self.player.y = y

    

    # <summary>
    # Observations received
    # </summary>
    # <param name="o">list of observations</param>
    def GetObservations(self, o):

        #cmd = "";
        for s in o:
        
            if s == "blocked":
                pass
            
            elif s == "steps":
                pass
            
            elif s == "breeze":
                pass

            elif s == "flash":
                pass

            elif s == "blueLight":
                pass

            elif s == "redLight":
                pass

            elif s == "greenLight":
                pass

            elif s == "weakLight":
                pass


    # <summary>
    # No observations received
    # </summary>
    def GetObservationsClean(self):
        pass
    

    # <summary>
    # Get Decision
    # </summary>
    # <returns>command string to new decision</returns>
    def GetDecision(self):

        n = random.randint(0,7)
        

        if n == 0:
            return "virar_direita"
        elif n == 1:
            return "virar_esquerda"
        elif n == 2:
            return "andar"
        elif n == 3:
            return "atacar"
        elif n == 4:
            return "pegar_ouro"
        elif n == 5:
            return "pegar_anel"
        elif n == 6:
            return "pegar_powerup"
        elif n == 7:
            return "andar_re"

        return ""

    def manhattan(self, pos1, pos2):
        if self.CheckNotOutOfBounds(pos1.x, pos1.y) and self.CheckNotOutOfBounds(pos2.x, pos2.y):
            return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)
        return None

    def CheckNotOutOfBounds(self,x,y):
            if x>58 or x<0 or y<0 or y>33:
                return False
            return True

    def GetCharPosition(self, pos):
        if self.CheckNotOutOfBounds(pos.x, pos.y):
            return self.map[pos.x][pos.y]
        return None
        
    def GetPositionRight(self):
        ret = None
        if self.dir == "north" and self.CheckNotOutOfBounds(self.player.x + 1, self.player.y):
            ret = Position(self.player.x + 1, self.player.y)      
        elif self.dir == "east" and self.CheckNotOutOfBounds(self.player.x, self.player.y + 1):
                ret = Position(self.player.x, self.player.y + 1)     
        elif self.dir == "south" and self.CheckNotOutOfBounds(self.player.x - 1, self.player.y):
                ret = Position(self.player.x - 1, self.player.y)    
        elif self.dir == "west" and self.CheckNotOutOfBounds(self.player.x, self.player.y - 1):
                ret = Position(self.player.x, self.player.y - 1)
        return ret

    def GetPositionLeft(self):
        ret = None
        if self.dir == "north" and self.CheckNotOutOfBounds(self.player.x - 1, self.player.y):
            ret = Position(self.player.x - 1, self.player.y)      
        elif self.dir == "east" and self.CheckNotOutOfBounds(self.player.x, self.player.y - 1):
                ret = Position(self.player.x, self.player.y - 1)     
        elif self.dir == "south" and self.CheckNotOutOfBounds(self.player.x + 1, self.player.y):
                ret = Position(self.player.x + 1, self.player.y)    
        elif self.dir == "west" and self.CheckNotOutOfBounds(self.player.x, self.player.y + 1):
                ret = Position(self.player.x, self.player.y + 1)
        return ret

      def GetPositionBehind(self):
        ret = None
        if self.dir == "north" and self.CheckNotOutOfBounds(self.player.x, self.player.y + 1):
            ret = Position(self.player.x, self.player.y + 1)      
        elif self.dir == "east" and self.CheckNotOutOfBounds(self.player.x - 1, self.player.y):
                ret = Position(self.player.x - 1, self.player.y)     
        elif self.dir == "south" and self.CheckNotOutOfBounds(self.player.x, self.player.y - 1):
                ret = Position(self.player.x, self.player.y - 1)    
        elif self.dir == "west" and self.CheckNotOutOfBounds(self.player.x + 1, self.player.y):
                ret = Position(self.player.x + 1, self.player.y)
        return ret

    def GetPositionForward(self):
        ret = None
        if self.dir == "north" and self.CheckNotOutOfBounds(self.player.x, self.player.y - 1):
            ret = Position(self.player.x, self.player.y - 1)      
        elif self.dir == "east" and self.CheckNotOutOfBounds(self.player.x + 1, self.player.y):
            ret = Position(self.player.x + 1, self.player.y)     
        elif self.dir == "south" and self.CheckNotOutOfBounds(self.player.x, self.player.y + 1):
            ret = Position(self.player.x, self.player.y + 1)    
        elif self.dir == "west" and self.CheckNotOutOfBounds(self.player.x - 1, self.player.y):
            ret = Position(self.player.x - 1, self.player.y)
        return ret

    def IsPositionSafe(self, position):
        if position == "Forward":
            next_position = self.GetPositionForward()
        elif position == "Behind":
            next_position = self.GetPositionBehind()
        elif postion == "Left":
            next_position = self.GetPositionLeft()
        else:
            next_position = self.GetPositionRight()
        if next_position:
            return self.GetCharPosition(position_forward) != "!"

     def GetAllPowerupsPositions(self):
        powerups_positions = []
        for y in range(34):
            for x in range(59):
                if self.map[x][y] == "L":
                    powerups_positions.append(Position(x,y))
        return powerups_positions

     def FindNearestPowerup(self):
        powerups_positions = self.GetAllPowerupsPositions()
        nearest_powerup = None
        min_distance = 1000000
        current_position = self.GetPlayerPosition()
        for powerup_position in powerups_positions:
            dist_to_powerup = self.manhattan(powerup_position, current_position)
            if dist_to_powerup < min_distance:
                nearest_powerup = powerup_position
                min_distance = dist_to_powerup
        if not self.EqualPositions(nearest_powerup, self.GetPowerupPositionBeingSearched()):
            self.SetPowerupPositionBeingSearched(nearest_powerup)
        return nearest_powerup

     def GetAllGoldsPositions(self):
        golds_positions = []
        for y in range(34):
            for x in range(59):
                if self.map[x][y] == "T":
                    golds_positions.append(Position(x,y))
        return golds_positions

    def FindNearestGold(self):
        golds_positions = self.GetAllGoldsPositions()       
        nearest_gold = None
        min_distance = 1000000
        current_position = self.GetPlayerPosition()
        for gold_position in golds_positions:
            dist_to_gold = self.manhattan(gold_position, current_position)
            if dist_to_gold < min_distance and not self.IsGoldPositionTimedOut(gold_position):
                nearest_gold = gold_position
                min_distance = dist_to_gold
        if not self.EqualPositions(nearest_gold, self.GetGoldPositionBeingSearched()):
            self.SetGoldPositionBeingSearched(nearest_gold)
        return nearest_gold



   

    

            
        
       
    

    

    

    


    

