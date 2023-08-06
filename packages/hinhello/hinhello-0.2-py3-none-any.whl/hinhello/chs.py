import hinhello.api as h
import click

@click.command()
@click.option('-c', default=1, help='bir yada yada iki yazarak hello veya hi yazdirabilirsiniz')
def main(c):
   if c==1:
      h.hellofunc()
      print("*1*")
   else:
      h.hifunc()
      print("*2*")

if __name__ == "__main__":
      main()