from random import randint
from itertools import product
import scene, ui

from pprint import pprint


class Block(scene.ShapeNode):
  def __init__(self, _r, _c):
    super(Block,self).__init__()
    self.x = _r
    self.y = _c
    self.wall = False
    self.fixed = False
    self.active = False
    
  def is_wall(self):
    self.fill_color = 'black'
    # fixme: いらないかも
    self.wall = True


class TetrisMain(scene.Node):
  def __init__(self, row, clo, size):
    super(TetrisMain,self).__init__()
    self.row = row
    self.clo = clo
    size_x, size_y = size
    self._w = size_x*.88
    self._h = size_y*.72
    self.bw = self._w/self.row
    self.bh = self._h/self.clo
    self.default_color = 'dimgray'
    self.fixed_line = []
    self.create_blocks()
    
  def create_blocks(self):
    # fixme: 全ブロックを生成
    self.block = [[self.set_block(r,c) for c in range(self.clo)]for r in range(self.row)]
  
  def set_block(self, r, c):
    path = ui.Path.rounded_rect(0, 0, self.bw, self.bh, 4)
    _block = Block(r,c)
    _block.path = path
    _block.fill_color = self.default_color
    _block.alpha = .5
    _block.position = (
      _block.x*self.bw, _block.y*self.bh
      )
    # todo: top の非表示blocks
    if not(_block.y > self.clo-3):
      self.add_child(_block)
    # todo: 外壁作成
    if _block.x == 0 or _block.y == self.clo-3:
      if _block.x < 3 or _block.x > self.row-4:
        _block.is_wall()
    if _block.x == self.row-1:
      _block.is_wall()
    if _block.y == 0:
      _block.is_wall()
      self.fixed_line += [_block.x,_block.y],
    
    # todo: debug 用 (座標出す)
    num = scene.LabelNode(f'{r},{c}', font = ('Ubuntu Mono', 10))
    _block.add_child(num)
    
    return _block
    
  def drop_minos(self):
    # fixme: 射出位置、要検討
    drop_x =int(self.row / 2)-1
    doro_y=int(self.clo -2)
    minos = self.create_minos(drop_x, doro_y)
    put_minos = []
    for mino in minos[:-1]:
      r, c = mino
      self.block[r][c].fill_color = minos[-1]
      self.block[r][c].active = True
      put_minos += [r, c],
    return put_minos
    
  def create_minos(self, drop_x, doro_y):
    x = drop_x
    y = doro_y
    mino_i = [[x-1,y],[x,y],
              [x+1,y],[x+2,y],
              'cyan']
    mino_o = [[x,y],[x,y+1],
              [x+1,y],[x+1,y+1],
              'yellow']
    mino_s = [[x,y],[x+1,y],
              [x+1,y+1],[x+2,y+1],
              'green']
    mino_z = [[x+1,y],[x+2,y],
              [x+1,y+1],[x,y+1],
              'red']
    mino_j = [[x,y],[x+1,y],
              [x+2,y],[x,y+1],
              'blue']
    mino_l = [[x,y],[x+1,y],
              [x+2,y],[x+2,y+1],
              'orange']
    mino_t = [[x,y],[x+1,y],
              [x+2,y],[x+1,y+1],
              'purple']
    all = [mino_i, mino_o, mino_s,
             mino_z, mino_j, mino_l,
             mino_t]
    return all[randint(0,len(all)-1)]
    

class MainScene(scene.Scene):
  def setup(self):
    clo = 24
    row = 12
    self.background_color = 'darkslategray'
    self.tm = TetrisMain(row, clo, self.size)
    self.tm.position = (
      self.size[0]*.5 - self.tm.bbox[2]*.5 + self.tm.bw*.5,
      self.size[1]*.5 - self.tm.bbox[3]*.5 + self.tm.bh*2
      )
    self.add_child(self.tm)
    self.put_minos = self.tm.drop_minos()
    
    # --- btn start
    self.btn = scene.ShapeNode()
    self.btn.path = ui.Path.oval(0,0,88,88)
    self.btn.position = self.size*.5
    self.btn.position -= (
      0,
      self.size[1]/2-self.btn.size[1]/1.28
      )
    self.add_child(self.btn)
    # --- btn end
    
  def touch_began(self, touch):
    if touch.location in (self.btn.frame):
      self.btn.alpha = .5
      self.take_minos = []
      for b in self.put_minos:
        x, y = b
        y -= 1
        self.take_minos += [x, y],
      for t, p in product(self.take_minos,self.tm.fixed_line):
        if t == p:
          self.tm.fixed_line += self.put_minos
          self.put_minos = self.tm.drop_minos()
          break
      else:
        for take, put in zip(self.take_minos,self.put_minos):
          tx, ty = take
          px, py = put
          take_block = self.tm.block[tx][ty]
          put_block = self.tm.block[px][py]
          set_color = put_block.fill_color
          take_block.fill_color = set_color
          put_block.fill_color = self.tm.default_color
        self.put_minos = self.take_minos
        
  def touch_ended(self, touch):
    if touch.location in (self.btn.frame):
      self.btn.alpha = 1

main = MainScene()
scene.run(main,
          orientation='PORTRAIT',
          frame_interval=2,
          show_fps=True)

