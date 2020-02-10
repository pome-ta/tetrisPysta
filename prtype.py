from random import randint
from itertools import product
import scene, ui

from pprint import pprint


# 重力という概念 🤔 (block落とし先表現とかは楽よね)
class Block(scene.ShapeNode):
  def __init__(self, _r, _c):
    super(Block,self).__init__()
    self.x = _r
    self.y = _c
    self.b_pos = [self.x, self.y]
    self.wall = False
    self.fixed = False
    self.blank = True
    
  def is_wall(self,color):
    self.fill_color = color
    # todo: いらないかも
    self.wall = True
  
  def is_fixed(self):
    self.fixed = True
    
  def is_blank(self,color):
    self.fill_color = color
    self.blank = True


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
    self.wall_line = []
    self.fixed_block = []
    
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
    # fixme: 非表示blocks addしないとか ?
    # todo: 外壁作成
    '''
    if not(_block.y > self.clo-3):
      self.add_child(_block)
    '''
    self.add_child(_block)
    if _block.x < 3:
      if _block.y > self.clo-4 or _block.x == 0:
        self.wall_line += [_block.x,_block.y],
        _block.is_wall('black')
    if _block.x > self.row-4:
      if _block.y > self.clo-4 or _block.x == self.row-1:
        self.wall_line += [_block.x,_block.y],
        _block.is_wall('black')
    if _block.y == 0:
      self.wall_line += [_block.x,_block.y],
      _block.is_wall('black')
    
    
    # todo: debug 用 (座標出す)
    num = scene.LabelNode(f'{r},{c}', font = ('Ubuntu Mono', 10))
    _block.add_child(num)
    
    return _block
    
  def drop_minos(self):
    # fixme: 射出位置、要検討
    #drop_x =int(self.row / 2)-1
    #doro_y=int(self.clo -2)
    
    drop_x =int(self.row / 2)-1
    doro_y=int(self.clo/2)
    
    minos = self.create_minos(drop_x, doro_y)
    put_minos = []
    for mino in minos[:-1]:
      r, c = mino
      self.block[r][c].fill_color = minos[-1]
      self.block[r][c].active = True
      put_minos += [r, c],
    
    return put_minos
    
  def create_minos(self, drop_x, doro_y):
    bx = drop_x
    by = doro_y
    mino_i = [[bx-1,by],[bx,by],
              [bx+1,by],[bx+2,by],
              'cyan']
    mino_o = [[bx,by],[bx,by+1],
              [bx+1,by],[bx+1,by+1],
              'yellow']
    mino_s = [[bx,by],[bx+1,by],
              [bx+1,by+1],[bx+2,by+1],
              'green']
    mino_z = [[bx+1,by],[bx+2,by],
              [bx+1,by+1],[bx,by+1],
              'red']
    mino_j = [[bx,by],[bx+1,by],
              [bx+2,by],[bx,by+1],
              'blue']
    mino_l = [[bx,by],[bx+1,by],
              [bx+2,by],[bx+2,by+1],
              'orange']
    mino_t = [[bx,by],[bx+1,by],
              [bx+2,by],[bx+1,by+1],
              'purple']
    '''
    all = [mino_i, mino_o, mino_s,
             mino_z, mino_j, mino_l,
             mino_t]'''
    all = [mino_i, mino_o]
    return all[randint(0,len(all)-1)]
  
  def move_action(self):
    # fixme: 消す
    # fixme: 止ま(め)る
    # fixme: 動く(回る)
    pass
    
  def set_fixed_line(self, line):
    pass
    
  def delete_line(self,line):
    for c in line:
      d = c[1]
      u = c[1] + 1
      #print(u)
      while u <= 20:
        self.block[c[0]][d].fill_color = self.block[c[0]][u].fill_color
        print(u)
        d += 1
        u += 1
      self.block[c[0]][20].fill_color = 'red'
      
        
      
      '''
      d = self.block[c[0]][c[1]]
      if c[1] < 20:
        d.fill_color = 
      #print('r')
      '''
    
    
    

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
    self.take_minos = []
    
    self.fixed = self.tm.wall_line
    #print('wall_line:')
    #pprint(self.tm.wall_line)
    #self.tm.block[0][0].fill_color = 'red'
    
    # --- btn start
    self.btn = scene.ShapeNode()
    self.btn.path = ui.Path.oval(0,0,88,88)
    self.btn.position = self.size*.5
    self.btn.position -= (
      0,
      self.size[1]/2-self.btn.size[1]/1.28
      )
    self.add_child(self.btn)
    
    self.btn1 = scene.ShapeNode()
    self.btn1.path = ui.Path.oval(0,0,88,88)
    self.btn1.fill_color = 'red'
    self.btn1.position = self.size*.5
    self.btn1.position -= (
      +(self.btn1.size[0]),
      self.size[1]/2-self.btn1.size[1]/1.28
      )
    self.add_child(self.btn1)
    
    self.btn2 = scene.ShapeNode()
    self.btn2.path = ui.Path.oval(0,0,88,88)
    self.btn2.fill_color = 'blue'
    self.btn2.position = self.size*.5
    self.btn2.position -= (
      -(self.btn1.size[0]),
      self.size[1]/2-self.btn2.size[1]/1.28
      )
    self.add_child(self.btn2)
    # --- btn end
    
  def update(self):
    pass
  def did_evaluate_actions(self):
    pass
    # ライン判断
    
    # --- --- ---
    
    
    
  def touch_began(self, touch):
    fnc_minos = self.put_minos
    if touch.location in (self.btn.frame):
      self.btn.alpha = .5
      self.down_action(fnc_minos)
    if touch.location in (self.btn1.frame):
      self.btn1.alpha = .5
      self.put_minos = self.l_action(fnc_minos)
    if touch.location in (self.btn2.frame):
      self.btn2.alpha = .5
      self.put_minos = self.r_action(fnc_minos)
        
  def touch_ended(self, touch):
    if touch.location in (self.btn.frame):
      self.btn.alpha = 1
    if touch.location in (self.btn1.frame):
      self.btn1.alpha = 1
    if touch.location in (self.btn2.frame):
      self.btn2.alpha = 1


  def down_action(self, fnc_minos):
    put_minos = fnc_minos
    self.fixed = self.tm.wall_line
    take_minos = self.take_minos
    take_minos = []
    for r in put_minos:
      xr, yr = r
      yr -= 1
      take_minos += [xr, yr],
    minos_len = len(put_minos)
    set_minos = put_minos + take_minos
    set_color = self.tm.block[put_minos[0][0]][put_minos[0][1]].fill_color
    self.fixed += self.tm.fixed_block
    for take, fix in product(take_minos, self.fixed):
      if take == fix:
        self.tm.fixed_block += self.put_minos
        self.put_minos = self.tm.drop_minos()
        self.tm.fixed_block.sort()
        for f in put_minos:
          self.tm.block[f[0]][f[1]].is_fixed()
        for line in self.tm.fixed_block:
          if line[0] == 1:
            b_cnt = []
            for fst in range(1,11):
              if self.tm.block[fst][line[1]].fixed:
                b = self.tm.block[fst][line[1]].b_pos
                b_cnt+= b,
                if len(b_cnt) == 10:
                  for c in b_cnt:
                    self.tm.fixed_block.remove(c)
                    d = c[1]
                    u = c[1] + 1
                    while u <= 20:
                      # fixed と blank 管理
                      # 元 = 上
                      #self.tm.fixed_block.remove([c[0],d])
                      #print([c[0],d])
                      
                      self.tm.block[c[0]][d].fill_color = self.tm.block[c[0]][u].fill_color
                      self.tm.block[c[0]][d].fixed = self.tm.block[c[0]][u].fixed
                      
                      
                      if self.tm.block[c[0]][d].fixed:
                        self.tm.fixed_block += [c[0],d],
                      
                      d += 1
                      u += 1
                    self.tm.block[c[0]][20].fill_color = 'red'
                    self.tm.block[c[0]][20].fixed = False
        break
    else:
      for n, i in enumerate(set_minos):
        if n < minos_len:
          self.tm.block[i[0]][i[1]].is_blank('dimgray')
        else:
          self.tm.block[i[0]][i[1]].fill_color = set_color
          
      self.put_minos = take_minos
    
    return self.put_minos
  


  def l_action(self, fnc_minos):
    put_minos = fnc_minos
    self.fixed = self.tm.wall_line
    take_minos = self.take_minos
    take_minos = []
    for r in put_minos:
      xr, yr = r
      xr -= 1
      take_minos += [xr, yr],
    minos_len = len(put_minos)
    set_minos = put_minos + take_minos
    set_color = self.tm.block[put_minos[0][0]][put_minos[0][1]].fill_color
    self.fixed += self.tm.fixed_block
    for take, fix in product(take_minos, self.fixed):
      if take == fix:
        self.put_minos = put_minos
        break
    else:
      for n, i in enumerate(set_minos):
        if n < minos_len:
          self.tm.block[i[0]][i[1]].fill_color = self.tm.default_color
        else:
          self.tm.block[i[0]][i[1]].fill_color = set_color
      self.put_minos = take_minos
    return self.put_minos
  
  def r_action(self, fnc_minos):
    put_minos = fnc_minos
    self.fixed = self.tm.wall_line
    take_minos = self.take_minos
    take_minos = []
    for r in put_minos:
      xr, yr = r
      xr += 1
      take_minos += [xr, yr],
    minos_len = len(put_minos)
    set_minos = put_minos + take_minos
    set_color = self.tm.block[put_minos[0][0]][put_minos[0][1]].fill_color
    self.fixed += self.tm.fixed_block
    for take, fix in product(take_minos, self.fixed):
      if take == fix:
        self.put_minos = put_minos
        break
    else:
      for n, i in enumerate(set_minos):
        if n < minos_len:
          self.tm.block[i[0]][i[1]].fill_color = self.tm.default_color
        else:
          self.tm.block[i[0]][i[1]].fill_color = set_color
      self.put_minos = take_minos
    return self.put_minos
    

main = MainScene()
scene.run(main,
          orientation='PORTRAIT',
          frame_interval=2,
          show_fps=True)
