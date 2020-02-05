import random
import scene, ui
from pprint import pprint


class Block(scene.ShapeNode):
  def __init__(self,_r,_c):
    super(Block,self).__init__()
    self.x = _r
    self.y = _c
    self.wall = False
    self.fixed = False
    self.active = False
    
  def is_wall(self):
    self.fill_color = 'black'
    self.wall = True


class Blocks(scene.Node):
  def __init__(self, row, clo, size):
    super(Blocks,self).__init__()
    self.row = row
    self.clo = clo
    size_x, size_y = size
    self._w = size_x*.88
    self._h = size_y*.72
    self.bw = self._w/self.row
    self.bh = self._h/self.clo
    self.default_color = 'dimgray'
    self.create_blocks()
    
  def create_blocks(self):
    # fixme: 全ブロックを生成
    self.block = [[self.set_block(r,c) for c in range(self.clo)]for r in range(self.row)]
  
  def set_block(self,r,c):
    num = scene.LabelNode(f'{r},{c}',font = ('Ubuntu Mono',10))
    path = ui.Path.rounded_rect(0, 0, self.bw, self.bh, 4)
    _block = Block(r,c)
    _block.path = path
    _block.fill_color = self.default_color
    _block.alpha = .5
    _block.add_child(num)
    _block.position = (_block.x*self.bw,_block.y*self.bh)
    # fixme: 非表示blocks addしないとか ?
    self.add_child(_block)
    if _block.x == 0 or _block.y == self.clo-3:
      if _block.x < 3 or _block.x > self.row-4:
        _block.is_wall()
    if _block.y == 0 or _block.x == self.row-1:
      _block.is_wall()
    return _block
    
  def drop_minos(self):
    # fixme: 射出位置、要検討
    drop_x =int(self.row/2)-1
    doro_y=int(self.clo-2)
    minos = self.create_minos(drop_x,doro_y)
    push_minos = []
    for mino in minos[:-1]:
      r = mino[0]
      c = mino[1]
      self.block[r][c].fill_color = minos[-1]
      self.block[r][c].active = True
      push_minos += (r,c),
    return push_minos
    
  def create_minos(self,drop_x,doro_y):
    x = drop_x
    y = doro_y
    mino_i = [[x-1,y],[x,y],[x+1,y],[x+2,y],'cyan']
    mino_o = [[x,y],[x,y+1],[x+1,y],[x+1,y+1],'yellow']
    mino_s = [[x,y],[x+1,y],[x+1,y+1],[x+2,y+1],'green']
    mino_z = [[x+1,y],[x+2,y],[x+1,y+1],[x,y+1],'red']
    mino_j = [[x,y],[x+1,y],[x+2,y],[x,y+1],'blue']
    mino_l = [[x,y],[x+1,y],[x+2,y],[x+2,y+1],'orange']
    mino_t = [[x,y],[x+1,y],[x+2,y],[x+1,y+1],'purple']
    
    minos_all = [mino_i,mino_o,mino_s,mino_z,mino_j,mino_l,mino_t]
    return minos_all[random.randint(0,len(minos_all)-1)]
    


class MainScene(scene.Scene):
  def setup(self):
    clo = 24
    row = 12
    self.background_color = 'darkslategray'
    self.blocks = Blocks(row,clo,self.size)
    self.blocks.position = (self.size[0]*.5-self.blocks.bbox[2]*.5+self.blocks.bw*.5,
    self.size[1]*.5-self.blocks.bbox[3]*.5+self.blocks.bh*2)
    self.add_child(self.blocks)
    self.push_minos = self.blocks.drop_minos()
    self.blocks.block[0][0].fill_color = 'red'
    
    # --- btn
    self.btn = scene.ShapeNode()
    self.btn.path = ui.Path.oval(0,0,88,88)
    self.btn.position = self.size*.5
    self.btn.position -= (0,self.size[1]/2-self.btn.size[1]/1.28)
    self.add_child(self.btn)
    
  def touch_began(self, touch):
    if touch.location in (self.btn.frame):
      self.btn.alpha = .5
      self.pull_minos = self.push_minos
      count = 0
      for i in self.pull_minos:
        x_af,y_af = x_be, y_be = i
        be_minos = self.blocks.block[x_be][y_be]
        if not be_minos.wall:
          y_af -= 1
          af_minos = self.blocks.block[x_af][y_af]
          set_color = be_minos.fill_color
          be_minos.fill_color = self.blocks.default_color
          af_minos.fill_color = set_color
          
          self.pull_minos[count] = (x_af,y_af)
          count+=1
          
        
    
  def touch_ended(self, touch):
    if touch.location in (self.btn.frame):
      self.btn.alpha = 1

main = MainScene()
scene.run(main,
          orientation='PORTRAIT',
          frame_interval=2,
          show_fps=True)
