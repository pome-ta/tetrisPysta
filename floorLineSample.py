from pprint import pprint


div_x = 10
div_y = 20
floor_line = [l for l in range(div_x)]
n = (div_x * div_y)-int(div_x/2)-1

def create_mino(n):
  mino = [n,n+1,n+2,n+3]
  return mino




print('# ------ Start')

while 1:
  mino_i = create_mino(n)
  print(mino_i)
  if n > 0:
    n = n-10
  else:
    n = 0
  if (set(floor_line)&set(mino_i)):
    break
    

print(f'floor_line:{floor_line}')
print('# ------ End')


