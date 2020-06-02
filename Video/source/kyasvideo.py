from manimlib.imports import *


class Opener(Scene):
    def construct(self):
        img = ImageMobject('kyas logo.png')
        text1 = TextMobject("Welcome to Kyas Coin")
        text2 = TextMobject("Firstly: What is KyasCoin?")
        self.play(FadeIn(img))
        self.wait()
        self.play(ApplyMethod(img.shift, UP))
        text1.shift(DOWN)
        self.play(Write(text1))
        self.wait()
        self.play(FadeOut(img), FadeOut(text1))


class WhatIsKyas(Scene):
    def construct(self):
        text1 = TextMobject("Firstly: What is KyasCoin?")
        text2 = TextMobject("KyasCoin")

        el1 = TextMobject("Decentralised Cryptocurrency").set_color(RED)
        el2 = TextMobject("Deflationary Mechanism").set_color(ORANGE)
        el3 = TextMobject("Python Core").set_color(GREEN)
        el4 = TextMobject("JavaFx, Android and CLI Clients").set_color(BLUE)
        el5 = TextMobject("Free Signup Bonus Coins").set_color(PURPLE)
        el_group = VGroup(el1, el2, el3, el4, el5)

        for el in el_group:
            el.align_to(el1, LEFT)

        el1.shift(2 * UP)
        el2.shift(UP)
        el4.shift(DOWN)
        el5.shift(2 * DOWN)

        braces = Brace(el_group, LEFT)

        self.play(Write(text1))
        self.play(Transform(text1, text2))
        text1.remove()
        self.play(ApplyMethod(text1.next_to, braces, LEFT))
        self.play(GrowFromCenter(braces))
        for el in el_group:
            self.play(Write(el))
        self.wait()
        self.play(Uncreate(braces), Uncreate(text1), Uncreate(el_group))
        self.wait()


class Cryptocurrency(Scene):
    main_title = 0

    def construct(self):

        self.titles()
        self.dissect_block()
        self.stack_blocks()

        self.wait()

    def titles(self):

        self.main_title = TextMobject("Now: What is a Cryptocurrency?")
        self.main_title.set_color(RED)

        self.play(Write(self.main_title))
        self.play(ApplyMethod(self.main_title.shift, UP * 3))

        text2 = TextMobject("Blockchain Technology")
        self.play(Write(text2))
        self.play(Uncreate(text2))

    def dissect_block(self):
        block = Square(side_length=1)

        b = TexMobject("\\textit{B}")

        block.add(b)

        self.play(ShowCreation(block))
        self.play(ApplyMethod(block.shift, LEFT * 3))

        arrow = Arrow(LEFT)
        arrow.next_to(block, RIGHT)
        self.play(ShowCreation(arrow))

        blockimage = ImageMobject("block_structure.png")
        blockimage.next_to(arrow, RIGHT)
        self.play(ShowCreation(blockimage))

        self.wait()

        self.play(Uncreate(block), Uncreate(arrow), FadeOut(blockimage))

    def stack_blocks(self):
        blocks = []
        for i in range(12):
            blocks.append(Square(side_length=0.5))
            blocks[i].add(TexMobject("\\textit{B}"))


        global prev_block
        prev_block = 0

        for i in blocks:
            self.play(ShowCreation(i))

            if prev_block is 0:
                self.play(ApplyMethod(i.shift, LEFT * 5, DOWN))
            else:
                self.play(ApplyMethod(i.next_to, prev_block))

            prev_block = i

        self.wait()

        for j in blocks:
            self.play(j.move_to, blocks[0])

        for b in blocks:
            if b is not blocks.__getitem__(0):
                self.remove(b)




        self.play(ApplyMethod(blocks.__getitem__(0).move_to, ORIGIN))

        chain = Rectangle()
        chain.add(TexMobject("\\textit{Blockchain}"))

        self.play(Transform(blocks.__getitem__(0), chain))

        self.wait()


        self.play(Uncreate(blocks.__getitem__(0)), Uncreate(self.main_title))



class Deflation(GraphScene):
    main_title = []

    CONFIG = {
        "x_min": 0,
        "x_max": 15,
        "y_min": 0,
        "y_max": 21,
        "graph_origin": LEFT*4.5 + DOWN*3,
        "function_color": RED,
        "axes_color": WHITE,
        "x_tick_frequency": 15,
        "y_tick_frequency": 21,
        "x_axis_label": "$Time$",
        "y_axis_label": "$Coins$",
        "y_axis_height": 5,
    }

    def construct(self):
        self.titles()
        self.graph()
        self.burn_coin()
        self.wait()

    def titles(self):
        self.main_title = TextMobject("The Deflation Mechanism").set_color(ORANGE)
        self.play(Write(self.main_title))
        self.play(ApplyMethod(self.main_title.shift, UP*3))

    def graph(self):
        self.setup_axes(animate=True)



        func_graph = self.get_graph(self.exp_func, self.function_color)

        self.play(ShowCreation(func_graph))

        self.wait()

        self.play(Uncreate(func_graph), Uncreate(self.axes))

    def exp_func(self, x):
        return np.e.__pow__(-0.25*x+3)


class Burn(Scene):

    def construct(self):
        self.titles()
        self.burn_coin()

        self.wait()

    def titles(self):
        self.main_title = TextMobject("Coin Burning").set_color(ORANGE)
        self.play(Write(self.main_title))
        self.play(ApplyMethod(self.main_title.shift, UP*3))

    def burn_coin(self):
        coin = Circle().set_color(WHITE)
        coin.add(TexMobject("\\textit{KYS}"))
        self.play(FadeIn(coin))
        self.play(ApplyMethod(coin.shift, LEFT*3))


        burn = Square(side_length = 2).set_color(RED)
        burn_text = TexMobject("\\textit{Burn}")
        burn.add(burn_text)
        self.play(ShowCreation(burn))
        self.play(ApplyMethod(burn.shift, RIGHT*3))
        self.play(ApplyMethod(burn.remove, burn_text))


        mult = TexMobject("\\textbf{x 2,000,000}")
        mult.next_to(coin, DOWN)
        self.play(ApplyMethod(coin.add, mult))
        anims = []
        self.play(ApplyMethod(coin.shift, RIGHT*6))
        self.play(ShrinkToCenter(coin))

        self.play(Write(burn_text))


class KeyFacts(Scene):

    main_title = []

    def construct(self):
        self.titles()
        self.brace()
        self.play(Uncreate(self.main_title))
        self.wait()

    def titles(self):
        self.main_title = TextMobject("Key Facts about KyasCoin")
        self.play(Write(self.main_title))
        self.play(ApplyMethod(self.main_title.shift, UP*3))


    def brace(self):
        text1 = TextMobject("KyasCoin")

        el1 = TextMobject("1,000,000,000 KYS total supply").set_color(RED)
        el2 = TextMobject("± 2,000,000 Coins burned every block").set_color(ORANGE)
        el3 = TextMobject("New block every ± 120 seconds").set_color(GREEN)
        el4 = TextMobject("GPL3.0 Licence").set_color(BLUE)
        el5 = TextMobject("600 KYS for every new user").set_color(PURPLE)
        el_group = VGroup(el1, el2, el3, el4, el5)

        for el in el_group:
            el.align_to(el1, LEFT)

        el1.shift(2 * UP)
        el2.shift(UP)
        el4.shift(DOWN)
        el5.shift(2 * DOWN)

        braces = Brace(el_group, LEFT)

        self.play(Write(text1))
        self.play(ApplyMethod(text1.next_to, braces, LEFT))
        self.play(GrowFromCenter(braces))
        for el in el_group:
            self.play(Write(el))
        self.wait()
        self.play(Uncreate(braces), Uncreate(text1), Uncreate(el_group))











