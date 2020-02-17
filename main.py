from random import randint
from itertools import product
import scene, ui
from pprint import pprint


class Block(scene.ShapeNode):
  def __init__(self, row, clo):
    super(Block,self).__init__()
    self.x = row
    self.y = clo
    self.b_pos = [self.x, self.y]
    self.wall = False
    self.fixed = False
    self.alpha = .5
    self.is_default()
    
  def is_default(self):
    self.fixed = False
    self.fill_color = 'dimgray'
  
  def is_active(self, color):
    self.fixed = False
    self.fill_color = color
    
  def is_wall(self):
    self.wall =True
    self.fill_color = 0
    
  def is_fixed(self):
    self.fixed = True
    
  def push(self):
    self.fill_color = self.fill_color
    self.fixed = self.fixed
    return self.fill_color, self.fixed
  
  def get(self, push):
    self.fill_color = push[0]
    self.fixed = push[1]
    

class TetrisMain(scene.Node):
  def __init__(self, parent_size):
    super(TetrisMain,self).__init__()
    self.row = 12#12
    self.clo = 24#24
    # todo: 大きくなると遅くなる
    self.play_speed = 2
    self.dt = 0.0
    self.parent_x, self.parent_y = parent_size
    self.w = self.parent_x*.92
    self.h = self.parent_y*.80
    self.bw = self.w/self.row
    self.bh = self.h/self.clo
    self.set_x = int(self.row/2)-1
    #self.start_y = int(self.clo -2)
    self.set_y = int(self.clo/2)
    self.set_root = [self.set_x, self.set_y]
    self.wall_bloks = []
    self.fixed_bloks =[]
    self.line_x = self.row-1
    self.line_y = self.clo-3
    self.start()
  
  def start(self):
    self.create_field()
    self.mino = self.push_mino(self.set_root)
    return self.mino
  
  def create_mino(self):
    all = self.types_mino()
    #return all[randint(0,len(all)-1)]
    return all[randint(0,1)]
    
  def push_mino(self, set_root):
    mino = self.create_mino()
    self.active_mino(mino, set_root)
    return mino
  
  def create_field(self):
    self.blocks = [[self.setup_blocks(r, c) for c in range(self.clo)]for r in range(self.row)]
    x_pos = (self.parent_x*.5
           - self.bbox[2]*.5
           + self.bw*.5)
    y_pos = (self.parent_y*.5
           - self.bbox[3]*.38
           + self.bh*.5)
    self.position = (x_pos, y_pos)
  
  def setup_blocks(self, r, c):
    block = Block(r,c)
    path = ui.Path.rounded_rect
    block.path = path(0, 0,
                 self.bw, self.bh, 8)
    block.position = (block.x*self.bw,
                      block.y*self.bh)
    self.set_wall(block)
    ''' top の2行消す
    if not(block.y > self.clo-3):
      self.add_child(block)
    '''
    self.add_child(block)
    # todo: debug 用 (座標出す)
    num = scene.LabelNode(f'{r},{c}',
          font = ('Ubuntu Mono', 10))
    num.color = 1
    num.alpha = 1
    block.add_child(num)
    return block
  
  def set_wall(self, block):
    if block.x < 3:
      if block.y > self.clo-4 or block.x == 0:
        self.wall_bloks.append(block.b_pos)
        block.is_wall()
    if block.x > self.row-4:
      if block.y > self.clo-4 or block.x == self.row-1:
        self.wall_bloks.append(block.b_pos)
        block.is_wall()
    if block.y == 0:
      self.wall_bloks.append(block.b_pos)
      block.is_wall()
  
  
  def formation_mino(self, name, rotate):
    pass
  
  def types_mino(self):
    # fixme: 回転を考慮して、'set' 処理を変える？
    # fixme: setup_mino(hoge) 作るか
    mino_i = {
      'name':'i',
      'root':[0,0],
      'set':[[-1,0],[0,0],[1,0],[2,0]],
      #'set':self.formation_mino(),
      'color':'cyan',
      'rotate':1,
      'id':0,}
    mino_o = {
      'name':'o',
      'root':[0,0],
      'set':[[0,0],[0,1],[1,0],[1,1]],
      'color':'yellow',
      'rotate':0,
      'id':1,}
    mino_s = {
      'name':'s',
      'root':[0,0],
      'set':[[0,0],[1,0],[1,1],[2,1]],
      'color':'green',
      'rotate':1,
      'id':2,}
    mino_z = {
      'name':'z',
      'root':[0,0],
      'set':[[1,0],[2,0],[1,1],[0,1]],
      'color':'red',
      'rotate':1,
      'id':3,}
    mino_j = {
      'name':'j',
      'root':[0,0],
      'set':[[0,0],[1,0],[2,0],[0,1]],
      'color':'blue',
      'rotate':1,
      'id':4,}
    mino_l = {
      'name':'l',
      'root':[0,0],
      'set':[[0,0],[1,0],[2,0],[2,1]],
      'color':'orange',
      'rotate':1,
      'id':5,}
    mino_t = {
      'name':'t',
      'root':[0,0],
      'set':[[0,0],[1,0],[2,0],[2,1]],
      'color':'purple',
      'rotate':3,
      'id':6,}
    return [mino_i, mino_o, mino_s, mino_z, mino_j, mino_l, mino_t]
    
  def rotate_minos(self, mino):
    # fixme: ここで、変えちゃだめみたい
    if mino['name'] == 'i':
      if mino['rotate'] == 1:
        mino['rotate'] = 0
        mino['set'] = [[0,1],[0,0],[0,-1],[0,-2]]
      else:
        mino['rotate'] = 1
        mino['set'] = [[-1,0],[0,0],[1,0],[2,0]]
    return mino
  
  def select_mino(self, mino, root=None):
    if not root:
      root = mino['root']
    sel_set = []
    mino['root'] = root
    for set in mino.get('set'):
      set = [x+y for x,y in zip(set, mino['root'])]
      sel_set.append(set)
    return sel_set
  
  def active_mino(self, mino, root):
    for set in self.select_mino(mino, root):
      bx, by = set
      self.blocks[bx][by].is_active(mino.get('color'))
    return mino
  
  def default_mino(self, mino, root=None):
    if not root:
      root = mino['root']
    for set in self.select_mino(mino, root):
      bx, by = set
      self.blocks[bx][by].is_default()
    
  def pre_mino(self, mino, n):
    # fixme: 回転は別処理かな？
    pre_set = []
    if n == 0:pre = [0,-1]
    if n == 1:pre = [-1,0]
    if n == 2:pre = [1,0]
    if n == 3:
      pre = [0,0]
      mino = self.rotate_minos(mino)
    root = mino.get('root')
    root = [x+y for x,y in zip(pre, root)]
    for set in mino.get('set'):
      set = [x+y for x,y in zip(set, root)]
      pre_set.append(set)
    fixed = self.wall_bloks + self.fixed_bloks
    for pos, fix in product(pre_set, fixed):
      if pos == fix:
        if n == 0:
          self.do_fixed(mino)
        return 0
        break
    return root
    
  def move_mino(self, mino, n):
    root = self.pre_mino(mino, n)
    if root:
      self.default_mino(mino)
      self.active_mino(mino,root)
  
  def do_fixed(self, mino):
    fixed = self.select_mino(mino)
    for fix in fixed:
      self.fixed_bloks.append(fix)
      bx, by = fix
      self.blocks[bx][by].is_fixed()
    self.check_line()
    self.mino = self.push_mino(self.set_root)
    return self.mino
  
  def check_line(self):
    for y in range(1, self.line_y):
      fix = []
      if self.blocks[1][y].fixed:
        for x in range(1, self.line_x):
          if self.blocks[x][y].fixed:
            fix.append([x, y])
            if len(fix) == self.row-2:
              self.clear_line(fix, self.fixed_bloks)
            else: continue
          else: continue
      else: continue
  
  def clear_line(self, fix, fixed_blocks):
    for set in fix:
      bx, by = set
      fixed_blocks.remove([bx,by])
      self.blocks[bx][by].is_default()
    self.down_blocks(by, fixed_blocks)
  
  def down_blocks(self, by, fixed_blocks):
    tby = by + 1
    for x in range(1, self.line_x):
      for y in range(tby, self.line_y):
        if y != self.line_y-1:
          self.blocks[x][y-1].get(self.blocks[x][y].push())
          if self.blocks[x][y-1].fixed:
            fixed_blocks.append([x,y-1])
            fixed_blocks.remove([x,y])
        else:
          self.blocks[x][y].is_default()
    self.check_line()
    self.fixed_bloks = fixed_blocks
    return self.fixed_bloks
  
  def cf(self):
    if self.play_speed == 1:
      self.play_speed = 500
    else: self.play_speed = 1
    
  def manage_update(self, main_dt):
    self.dt += main_dt
    if self.dt > self.play_speed:
      self.move_mino(self.mino, 0)
      
      self.dt = 0
  
  
      

class MainScene(scene.Scene):
  def setup(self):
    self.background_color = 'darkslategray'
    self.tetris = TetrisMain(self.size)
    self.add_child(self.tetris)
    
    # --- btn start
    path = ui.Path.oval(0,0,72,72)
    self.d_btn = scene.ShapeNode(path=path,parent=self,fill_color = 'white')
    self.d_btn.position = self.size*.5
    self.d_btn.position -= (0,
      self.size[1]/2-self.d_btn.size[1]/2)
    self.l_btn = scene.ShapeNode(path=path,parent=self,fill_color = 'red')
    self.l_btn.position = self.size*.5
    self.l_btn.position -= (
      +(self.l_btn.size[0]),
      self.size[1]/2-self.l_btn.size[1])
    self.r_btn = scene.ShapeNode(path=path,parent=self,fill_color='blue')
    self.r_btn.position = self.size*.5
    self.r_btn.position -= (
      -(self.r_btn.size[0]*1),
      self.size[1]/2-self.r_btn.size[1])
    self.e_btn = scene.ShapeNode(path=path,parent=self,fill_color = 'yellow')
    self.e_btn.position = self.size*.5
    self.e_btn.position -= (0,
      self.size[1]/2-self.e_btn.size[1]*1.5)
    # --- btn end
    
  def update(self):
    self.tetris.manage_update(self.dt)
    
  def touch_began(self, touch):
    if touch.location in (self.d_btn.frame):
      self.d_btn.alpha = .256
      self.tetris.move_mino(self.tetris.mino, 0)
    
    if touch.location in (self.l_btn.frame):
      self.l_btn.alpha = .256
      self.tetris.move_mino(self.tetris.mino, 1)
    
    if touch.location in (self.r_btn.frame):
      self.r_btn.alpha = .256
      self.tetris.move_mino(self.tetris.mino, 2)
    
    if touch.location in (self.e_btn.frame):
      self.e_btn.alpha = .256
      self.tetris.move_mino(self.tetris.mino, 3)
        
  def touch_ended(self, touch):
    if touch.location in (self.d_btn.frame):
      self.d_btn.alpha = 1
    if touch.location in (self.l_btn.frame):
      self.l_btn.alpha = 1
    if touch.location in (self.r_btn.frame):
      self.r_btn.alpha = 1
    if touch.location in (self.e_btn.frame):
      self.e_btn.alpha = 1

main = MainScene()
scene.run(main,
          orientation='PORTRAIT',
          frame_interval=2,
          show_fps=True)

