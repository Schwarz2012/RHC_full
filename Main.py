from calendar import c
from turtle import circle
from kivy.app import App 
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.treeview import TreeView, TreeViewLabel, TreeViewNode
from kivy.config import Config
from kivy.lang.builder import Builder

from kivy.graphics import (Color, Ellipse, Rectangle, Line)
import Operations as oper
import Calculation as calc
import Collect_data as cd

from kivy.core.clipboard import Clipboard

#Config parametres
Config.set('input', 'mouse', 'mouse,disable_multitouch')
Window.maximize()
Window.clearcolor = (.12, .12, .12, 1)
#Window.clearcolor = (1, 1, 1, 0)

class MyBoxLayout(BoxLayout):
    pass
class GraphBoxLayout(BoxLayout, Widget):
    pass
class RotateBoxLayoutLeft(BoxLayout):
    pass
class RotateBoxLayoutRight(BoxLayout):
    pass
class MyTextInput(TextInput):
    multiline = False
    input_filter = 'float'
class MyFloatLayout(FloatLayout, Widget):
    pass
class MyLabel(Label):
    pass
class MyGridLayout(GridLayout):
    pass
class MyGridLayout2(GridLayout):
    pass



Builder.load_string('''
<MyBoxLayout>:
    canvas.before:
        Color:
            rgba: .1, .1, .1, 1
        Line:
            width: 1.3
            rectangle: self.x, self.y, self.width, self.height

<GraphBoxLayout>:
    canvas.before:

        Color:
            rgba: .3, .3, .3, 1
        Rectangle:
            size: self.size
            pos: self.pos 
        Color:
            rgba: 1, 1, 1, 1
        Line:
            circle: self.x, self.y, 3

<RotateBoxLayoutLeft>:
    canvas.before:
        PushMatrix
        Rotate:
            angle: 90
            origin: self.center
    canvas.after:
        PopMatrix

<RotateBoxLayoutRight>:
    canvas.before:
        PushMatrix
        Rotate:
            angle: -90
            origin: self.center
    canvas.after:
        PopMatrix


<MyLabel>:
    canvas.before:
        Color: 
            rgba: .1, .1, .1, 1
        Rectangle:
            size: self.size
            pos: self.pos   
    text_size: self.size
    halign: 'left'
    valign: 'middle'
    font_size: '22'
<MyGridLayout>:
    canvas.before:
        Color: 
            rgba: .1, 0, 0, 1
        Rectangle:
            size: self.size
            pos: self.pos   
''')


class RHCApp(App):

    def __init__(self):
        super().__init__()
        self.model_tree = TreeView(root_options={'text': 'Model tree'})
        self.Room_node = self.model_tree.add_node(TreeViewLabel(text = 'Room'))
        self.model_tree.add_node(TreeViewLabel(text = 'Ceiling'), self.Room_node)
        self.model_tree.add_node(TreeViewLabel(text = 'Floor'), self.Room_node)
        self.model_tree.add_node(TreeViewLabel(text = 'Wall 1'), self.Room_node)
        self.model_tree.add_node(TreeViewLabel(text = 'Wall 2'), self.Room_node)
        self.model_tree.add_node(TreeViewLabel(text = 'Wall 3'), self.Room_node)
        self.model_tree.add_node(TreeViewLabel(text = 'Wall 4'), self.Room_node)
        self.model_tree.add_node(TreeViewLabel(text = 'Results'))
        #Window constructor
        self.base_layer = BoxLayout()
        #Left window
        self.Left_window = MyBoxLayout(orientation = 'vertical', size_hint=(.25, 1))
        #Label
        self.Left_window_label = GridLayout(cols = 1, row_force_default = True, row_default_height = 30, size_hint=(1, 1) )
        self.Left_window_label.add_widget(MyLabel(text = 'Model Builder'))
        self.Left_window.add_widget(self.Left_window_label)
        #TreeView
        self.model_tree.bind(selected_node = self.tree_click)
        self.model_tree.bind(selected_node = self.Build)
        self.Left_window_label.add_widget(self.model_tree)
        #Buttons RS and Op
        self.RS_OP_Button = BoxLayout(size_hint=(1, None))
        self.RS_OP_Button.add_widget(Button(text = 'Radiant\nsurface', size = (300, 40), size_hint=(1, None), on_press = self.RsCreate))
        self.RS_OP_Button.add_widget(Button(text = 'Window/Door', size = (300, 40), size_hint=(1, None), on_press = self.OpCreate))
        self.Left_window.add_widget(self.RS_OP_Button)
        #del
        self.Left_window.add_widget(Button(text = 'Delete', size = (300, 40), size_hint=(1, None), on_press = self.delete)) 
        #Left window to base layer
        self.base_layer.add_widget(self.Left_window)

        #Central window
        #Label
        self.central_window = MyBoxLayout(orientation = 'vertical',size_hint=(.25, 1))
        self.central_window_label = GridLayout(cols = 1, row_force_default = True, row_default_height = 30)
        self.central_window_label.add_widget(MyLabel(text = 'Settings'))
        self.central_window.add_widget(self.central_window_label)
        self.central_window_body = GridLayout(cols = 1, row_force_default = True, row_default_height = 50)
        self.central_window_label.add_widget(self.central_window_body)
        #Layers for different nodes
        self.central_corner_coordinate = GridLayout(cols = 3, row_force_default = True, row_default_height = 30)
        self.central_size_value = GridLayout(cols = 3, row_force_default = True, row_default_height = 30)
        self.central_window_phys_par = GridLayout(cols = 3, row_force_default = True, row_default_height = 30)
        self.central_window_space = BoxLayout(size_hint=(1, 1))
        self.time = BoxLayout()
        #Central window to base layer
        self.base_layer.add_widget(self.central_window)
        #Central window settings
        self.settings = GridLayout(cols = 2, row_force_default = True, row_default_height = 30)
        self.geomspinner = Spinner(text='m',values=('m', 'cm', 'mm'))
        self.tempspinner = Spinner(text='°C',values=('°C', 'K'))

        #Right window
        self.right_window = MyBoxLayout(orientation = 'vertical',size_hint=(.5, 1))   
        #Graphs
        self.right_window_graph = BoxLayout(orientation = 'vertical', size = (30, 30), size_hint=(1, None))
        self.right_window_graph_data = BoxLayout(orientation = 'vertical', size_hint=(1, 1))
        self.right_window_graph.add_widget(MyLabel(text = 'Graphics'))       
        self.right_window.add_widget(self.right_window_graph)
        self.right_window.add_widget(self.right_window_graph_data)
        self.up = BoxLayout(size_hint=(1, .05))

        self.left = RotateBoxLayoutLeft(size_hint=(.05, 1))

        self.right = RotateBoxLayoutRight(size_hint=(.05, 1))
        self.down = BoxLayout(size_hint=(1, .05))
        self.central_line = BoxLayout(size_hint=(1, .8))
        self.central_graph = BoxLayout(size_hint=(.9, 1))
        self.right_window_graph_data.add_widget(self.up)

        self.right_window_graph_data.add_widget(self.central_line)
        self.central_line.add_widget(self.left)
        self.central_line.add_widget(self.central_graph)  
        self.central_line.add_widget(self.right)
        self.right_window_graph_data.add_widget(self.down)

        #Results
        self.right_window_results = GridLayout(cols = 1, row_force_default = True, row_default_height = 30)
        self.right_window_results.add_widget(MyLabel(text = 'Results'))
        self.right_window_results_button = GridLayout(cols = 2, row_force_default = True, row_default_height = 30)
        self.right_window_results.add_widget(self.right_window_results_button)
        self.temp_btn = Button(text = 'Temperatures', on_press = self.tempresults,  size = (200, 40))
        self.heat_balance_btn = Button(text = 'Heat Balance',   on_press = self.hbresults, size = (200, 40))
        self.right_window_results_button.add_widget(self.temp_btn)
        self.right_window_results_button.add_widget(self.heat_balance_btn)
        self.right_window_results_data_layout = BoxLayout()

        self.leftlabel = Label(text = 'Wall 1 (Length)')
        self.rightlabel = Label(text = 'Wall 4 (Width)')


        self.right_window_results.add_widget(self.right_window_results_data_layout)

        self.right_window.add_widget(self.right_window_results)    
        #Right window to base layer
        self.base_layer.add_widget(self.right_window)

        #Menu labels
        self.labelEps = Label(text = 'Eps')
        self.unitEps = Label(text = '1')
        self.labelU = Label(text = 'U')
        self.unitU = Label(text = 'W/(K*m²)')
        self.labelTex = Label(text = 'Out temperature')
        self.labelTRS = Label(text = 'Surface temperature')
        self.unitTex = Label(text = '°C')
        self.LeftCornerLabel = Label(text = 'Left corner')    
        self.corner_x = Label(text = 'x')
        self.corner_y = Label(text = 'y')
        self.size = Label(text = 'Size')
        self.size_width = Label(text = 'Width')
        self.size_length = Label(text = 'Length')
        self.size_height = Label(text = 'Height')
        self.parlabel = Label(text = 'Physical parameters')
        self.Roomlabel = Label(text = 'Room geometry')
 


        #Wall
        self.WallParInput = {}
        self.WallOptionlabel = {}
        for i in range(1,5,1):
            self.WallOptionlabel[str(i)] = Label(text = 'Wall ' + str(i) + ' physical parameters' )
        for i in range(1,5,1):
            self.WallParInput['Eps' + str(i)] = MyTextInput(text = '0.9', size_hint_x=None, width=100)
            self.WallParInput['U' + str(i)] = MyTextInput( size_hint_x=None, width=100)
            self.WallParInput['Tex' + str(i)] = MyTextInput(size_hint_x=None, width=100 )          
        #Ceiling
        self.CeilingOptionlabel = Label(text = 'Ceiling  physical parameters')
        self.CeilingParInput = {}
        self.CeilingParInput['Eps'] = MyTextInput(text = '0.9', size_hint_x=None, width=100)      
        self.CeilingParInput['U'] = MyTextInput(size_hint_x=None, width=100)
        self.CeilingParInput['Tex'] = MyTextInput(size_hint_x=None, width=100)
        #Floor
        self.FloorOptionlabel = Label(text = 'Floor physical parameters')
        self.FloorParInput = {}
        self.FloorParInput['Eps'] = MyTextInput(text = '0.9', size_hint_x=None, width=100)      
        self.FloorParInput['U'] = MyTextInput(size_hint_x=None, width=100)
        self.FloorParInput['Tex'] = MyTextInput(size_hint_x=None, width=100)        
        #Room
        self.Room = {}
        self.Room['RL'] = MyTextInput(size_hint_x=None, width=100)
        self.Room['RL'].bind(text = self.room_resize)
        self.Room['RW'] = MyTextInput(size_hint_x=None, width=100)
        self.Room['RW'].bind(text = self.room_resize)
        self.Room['RH'] = MyTextInput(size_hint_x=None, width=100)
        #Result
        self.calc_btn = Button(text = 'Calculate', on_press = self.calculate, size = (200, 40), size_hint=(0.1, None))
        self.copy_btn = Button(text = 'Copy', on_press = self.copyresult, size = (200, 40), size_hint=(0.1, None))
        #RS
        self.build_btn = Button(text = 'Build', on_press = self.Build, size = (200, 40), size_hint=(0.1, None))      
        
        #Dicts and number of RS and Op
        #Walls RS
        self.wallrsnumber = [0, 0, 0, 0]
        self.wallRSlabel = {}
        self.wallRSpar = {}
        self.wallRScoord = {}
        self.wallRSdata = [[],[],[],[]]
        #Wall Op
        self.wallOpnumber = [0, 0, 0, 0]
        self.wallOplabel = {}
        self.wallOppar = {}
        self.wallOpcoord = {}
        self.wallOpdata = [[],[],[],[]]        
        #Ceiling RS
        self.Crsnumber = 0
        self.ceilingRSlabel = {}
        self.ceilingRSpar = {}
        self.ceilingRScoord = {}
        self.ceilingRSdata = []
        #Floor RS
        self.Frsnumber = 0
        self.floorRSlabel = {}
        self.floorRSpar = {}
        self.floorRScoord = {}
        self.floorRSdata = []
        #Result
        self.CopyCalcresult = ''
        self.resultclick = 0
      
    def RsCreate(self, *args):

        if self.model_tree.selected_node != None:
            Parent_name = self.model_tree.selected_node.text
            if ('Wall' in Parent_name) == True:
                    self.wallrsnumber[int(oper.number(Parent_name))-1] += 1
                    ind = self.wallrsnumber[int(oper.number(Parent_name))-1]                 
                    self.model_tree.add_node(TreeViewLabel(text= 'Radiant surface ' + str(ind), font_size = 14), self.model_tree.selected_node)
                    self.wallRSlabel[oper.number(Parent_name) + str(ind)] = Label(text = str(Parent_name) +  ' Radiant surface ' + str(ind), size = (100, 50))
                    self.wallRSpar[oper.number(Parent_name) + str(ind) + 'Eps'] = MyTextInput(text = '0.9', size_hint_x=None, width=100)
                    self.wallRSpar[oper.number(Parent_name) + str(ind) + 'TRS'] = MyTextInput(size_hint_x=None, width=100)
                    self.wallRScoord[oper.number(Parent_name) + str(ind) + 'x_corn'] = MyTextInput(size_hint_x=None, width=100)
                    self.wallRScoord[oper.number(Parent_name) + str(ind) + 'y_corn'] = MyTextInput(size_hint_x=None, width=100)
                    self.wallRScoord[oper.number(Parent_name) + str(ind) + 'Widht'] = MyTextInput(size_hint_x=None, width=100)
                    self.wallRScoord[oper.number(Parent_name) + str(ind) + 'Hight'] = MyTextInput(size_hint_x=None, width=100)
                    self.wallRScoord[oper.number(Parent_name) + str(ind) + 'Area'] = Label(text = '', size_hint_x=None, width=100)
                    self.wallRScoord[oper.number(Parent_name) + str(ind) + 'x_corn'].bind(text = self.Build)
                    self.wallRScoord[oper.number(Parent_name) + str(ind) + 'y_corn'].bind(text = self.Build)
                    self.wallRScoord[oper.number(Parent_name) + str(ind) + 'Widht'].bind(text = self.Build)
                    self.wallRScoord[oper.number(Parent_name) + str(ind) + 'Hight'].bind(text = self.Build)
                    self.wallRSdata[int(oper.number(Parent_name))-1].append(oper.number(Parent_name) + str(ind))
                    
            if ('Floor' in Parent_name) == True:
                    self.Frsnumber += 1
                    ind = self.Frsnumber
                    self.model_tree.add_node(TreeViewLabel(text= 'Radiant surface ' + str(ind), font_size = 14), self.model_tree.selected_node)
                    self.floorRSlabel['FloorRS' + str(ind)] = Label(text = str(Parent_name) +  ' Radiant surface ' + str(ind), size = (100, 50))
                    self.floorRSpar['FloorRS' + str(ind) + 'Eps'] = MyTextInput(text = '0.9', size_hint_x=None, width=100)
                    self.floorRSpar['FloorRS' + str(ind) + 'TRS'] = MyTextInput(size_hint_x=None, width=100)
                    self.floorRScoord['FloorRS' + str(ind) + 'x_corn'] = MyTextInput(size_hint_x=None, width=100)
                    self.floorRScoord['FloorRS' + str(ind) + 'y_corn'] = MyTextInput(size_hint_x=None, width=100)
                    self.floorRScoord['FloorRS' + str(ind) + 'Widht'] = MyTextInput(size_hint_x=None, width=100)
                    self.floorRScoord['FloorRS' + str(ind) + 'Length'] = MyTextInput(size_hint_x=None, width=100)
                    self.floorRScoord['FloorRS' + str(ind) + 'Area'] = Label(text = '', size_hint_x=None, width=100)
                    self.floorRScoord['FloorRS' + str(ind) + 'x_corn'].bind(text = self.Build)
                    self.floorRScoord['FloorRS' + str(ind) + 'y_corn'].bind(text = self.Build)
                    self.floorRScoord['FloorRS' + str(ind) + 'Widht'].bind(text = self.Build)
                    self.floorRScoord['FloorRS' + str(ind) + 'Length'].bind(text = self.Build)
                    self.floorRSdata.append(str(ind))
            if ('Ceiling' in Parent_name) == True:
                    self.Crsnumber += 1
                    ind = self.Crsnumber
                    self.model_tree.add_node(TreeViewLabel(text= 'Radiant surface ' + str(ind), font_size = 14), self.model_tree.selected_node)
                    self.ceilingRSlabel['CeilingRS' + str(ind)] = Label(text = str(Parent_name) +  ' Radiant surface ' + str(ind), size = (100, 50))
                    self.ceilingRSpar['CeilingRS' + str(ind) + 'Eps'] = MyTextInput(text = '0.9', size_hint_x=None, width=100)
                    self.ceilingRSpar['CeilingRS' + str(ind) + 'TRS'] = MyTextInput(size_hint_x=None, width=100)
                    self.ceilingRScoord['CeilingRS' + str(ind) + 'x_corn'] = MyTextInput(size_hint_x=None, width=100) 
                    self.ceilingRScoord['CeilingRS' + str(ind) + 'y_corn'] = MyTextInput(size_hint_x=None, width=100)
                    self.ceilingRScoord['CeilingRS' + str(ind) + 'Widht'] = MyTextInput(size_hint_x=None, width=100)
                    self.ceilingRScoord['CeilingRS' + str(ind) + 'Length'] = MyTextInput(size_hint_x=None, width=100)
                    self.ceilingRScoord['CeilingRS' + str(ind) + 'Area'] = Label(text = '', size_hint_x=None, width=100)
                    self.ceilingRScoord['CeilingRS' + str(ind) + 'x_corn'].bind(text = self.Build)
                    self.ceilingRScoord['CeilingRS' + str(ind) + 'y_corn'].bind(text = self.Build)
                    self.ceilingRScoord['CeilingRS' + str(ind) + 'Widht'].bind(text = self.Build)
                    self.ceilingRScoord['CeilingRS' + str(ind) + 'Length'].bind(text = self.Build)
                    self.ceilingRSdata.append(str(ind))
    def OpCreate(self, *args):
        if self.model_tree.selected_node != None:
            Parent_name = self.model_tree.selected_node.text
            if ('Wall' in Parent_name) == True:
                    self.wallOpnumber[int(oper.number(Parent_name))-1] += 1
                    ind = self.wallOpnumber[int(oper.number(Parent_name))-1]                 
                    self.model_tree.add_node(TreeViewLabel(text= 'Window/Door ' + str(ind), font_size = 14), self.model_tree.selected_node)
                    self.wallOplabel[oper.number(Parent_name) + str(ind)] = Label(text = str(Parent_name) + ' Window/Door ' + str(ind), size = (100, 50))
                    self.wallOppar[oper.number(Parent_name) + str(ind) + 'Eps'] = MyTextInput(text = '0.9', size_hint_x=None, width=100)
                    self.wallOppar[oper.number(Parent_name) + str(ind) + 'U'] = MyTextInput(size_hint_x=None, width=100)
                    self.wallOpcoord[oper.number(Parent_name) +str(ind) + 'x_corn'] = MyTextInput(size_hint_x=None, width=100)
                    self.wallOpcoord[oper.number(Parent_name) +str(ind) + 'y_corn'] = MyTextInput(size_hint_x=None, width=100)
                    self.wallOpcoord[oper.number(Parent_name) +str(ind) + 'Widht'] = MyTextInput(size_hint_x=None, width=100)
                    self.wallOpcoord[oper.number(Parent_name) +str(ind) + 'Hight'] = MyTextInput(size_hint_x=None, width=100)
                    self.wallOpcoord[oper.number(Parent_name) +str(ind) + 'Area'] = Label(text = '', size_hint_x=None, width=100)
                    self.wallOpcoord[oper.number(Parent_name) +str(ind) + 'x_corn'].bind(text = self.Build)
                    self.wallOpcoord[oper.number(Parent_name) +str(ind) + 'y_corn'].bind(text = self.Build)
                    self.wallOpcoord[oper.number(Parent_name) +str(ind) + 'Widht'].bind(text = self.Build)
                    self.wallOpcoord[oper.number(Parent_name) +str(ind) + 'Hight'].bind(text = self.Build)
                    self.wallOpdata[int(oper.number(Parent_name))-1].append(oper.number(Parent_name) + str(ind))

    def delete(self, obj):      
        if self.model_tree.selected_node != None:
            Select_name = self.model_tree.selected_node.text
            if ('Radiant' in Select_name) == True:
                    Parent_name = self.model_tree.selected_node.parent_node.text
                    if ('Wall' in Parent_name) == True:
                        self.wallRSdata[int(oper.number(Parent_name))-1].remove(oper.number(Parent_name) + oper.number(Select_name))
                    if ('Floor' in Parent_name) == True:
                        self.floorRSdata.remove(oper.number(Select_name))
                    if ('Ceiling' in Parent_name) == True:
                        self.ceilingRSdata.remove(oper.number(Select_name))
                    self.model_tree.remove_node(self.model_tree.selected_node)
                    self.central_window_body.clear_widgets()
            if ('Window/Door' in Select_name) == True:
                    Parent_name = self.model_tree.selected_node.parent_node.text
                    self.wallOpdata[int(oper.number(Parent_name))-1].remove(oper.number(Parent_name) + oper.number(Select_name))
                    self.model_tree.remove_node(self.model_tree.selected_node)
                    self.central_window_body.clear_widgets()


    def tree_click(self, *args):
        self.central_window_body.clear_widgets()
        self.central_window_phys_par.clear_widgets()
        self.central_corner_coordinate.clear_widgets()
        self.central_size_value.clear_widgets()
        self.central_graph.clear_widgets()
        self.up.clear_widgets()
        self.left.clear_widgets()
        self.right.clear_widgets()
        self.down.clear_widgets()
        self.settings.clear_widgets()
        self.RW = self.Room['RW'].text
        self.RL = self.Room['RL'].text
        self.RH = self.Room['RH'].text

        if self.model_tree.selected_node != None:
            Select_name = self.model_tree.selected_node.text
            if ('Wall' in Select_name) == True:
                self.central_window_body.add_widget(self.WallOptionlabel[oper.number(Select_name)])
                self.central_window_phys_par.add_widget(self.labelEps)
                self.central_window_phys_par.add_widget(self.WallParInput['Eps' + oper.number(Select_name)])
                self.central_window_phys_par.add_widget(self.unitEps)
                self.central_window_phys_par.add_widget(self.labelU)
                self.central_window_phys_par.add_widget(self.WallParInput['U' + oper.number(Select_name)])
                self.central_window_phys_par.add_widget(self.unitU)
                self.central_window_phys_par.add_widget(self.labelTex)
                self.central_window_phys_par.add_widget(self.WallParInput['Tex' + oper.number(Select_name)])
                self.central_window_phys_par.add_widget(Label(text = self.tempspinner.text))
                self.central_window_body.add_widget(self.central_window_phys_par)

            if ('Floor' in Select_name) == True:
                self.central_window_body.add_widget(self.FloorOptionlabel)
                self.central_window_phys_par.add_widget(self.labelEps)
                self.central_window_phys_par.add_widget(self.FloorParInput['Eps'])
                self.central_window_phys_par.add_widget(self.unitEps)
                self.central_window_phys_par.add_widget(self.labelU)
                self.central_window_phys_par.add_widget(self.FloorParInput['U'])
                self.central_window_phys_par.add_widget(self.unitU)
                self.central_window_phys_par.add_widget(self.labelTex)
                self.central_window_phys_par.add_widget(self.FloorParInput['Tex'])
                self.central_window_phys_par.add_widget(Label(text = self.tempspinner.text))
                self.central_window_body.add_widget(self.central_window_phys_par)

            if ('Ceiling' in Select_name) == True:
                self.central_window_body.add_widget(self.CeilingOptionlabel)
                self.central_window_phys_par.add_widget(self.labelEps)
                self.central_window_phys_par.add_widget(self.CeilingParInput['Eps'])
                self.central_window_phys_par.add_widget(self.unitEps)
                self.central_window_phys_par.add_widget(self.labelU)
                self.central_window_phys_par.add_widget(self.CeilingParInput['U'])
                self.central_window_phys_par.add_widget(self.unitU)
                self.central_window_phys_par.add_widget(self.labelTex)
                self.central_window_phys_par.add_widget(self.CeilingParInput['Tex'])
                self.central_window_phys_par.add_widget(Label(text = self.tempspinner.text))
                self.central_window_body.add_widget(self.central_window_phys_par)

            if ('Room' in Select_name) == True:
                self.central_window_body.add_widget(self.Roomlabel)
                self.central_size_value.add_widget(self.size_length)
                self.central_size_value.add_widget(self.Room['RL'])
                self.central_size_value.add_widget(Label(text = self.geomspinner.text))
                self.central_size_value.add_widget(self.size_width)
                self.central_size_value.add_widget(self.Room['RW'])
                self.central_size_value.add_widget(Label(text = self.geomspinner.text))
                self.central_size_value.add_widget(self.size_height)
                self.central_size_value.add_widget(self.Room['RH'])
                self.central_size_value.add_widget(Label(text = self.geomspinner.text))
                self.central_window_body.add_widget(self.central_size_value)
                self.up.add_widget(Label(text = 'Wall 2'))
                self.left.add_widget(self.leftlabel)
                self.right.add_widget(Label(text = 'Wall 3'))
                self.down.add_widget(self.rightlabel)
                self.graph = GraphBoxLayout()
                self.central_graph.add_widget(self.graph)

            if ('Result' in Select_name) == True:
                self.central_window_body.add_widget(self.calc_btn)
                self.central_window_body.add_widget(self.copy_btn)
                self.central_window_body.add_widget(self.time)

            if ('Model' in Select_name) == True:
                self.central_window_body.add_widget(Label(text = 'Model settings'))
                
                self.settings.add_widget(Label(text='Geometry units'))
                self.settings.add_widget(self.geomspinner)
                self.settings.add_widget(Label(text='Temperature units'))
                self.settings.add_widget(self.tempspinner)
                self.central_window_body.add_widget(self.settings)
    

                
            if ('Radiant' in Select_name) == True:
                Parent_name = self.model_tree.selected_node.parent_node.text
                if ('Wall' in Parent_name) == True:
                    wall_list = [1,2,3,4]
                    self.central_window_body.add_widget(self.wallRSlabel[oper.number(Parent_name) + oper.number(Select_name)])                   
                    self.central_window_body.add_widget(self.LeftCornerLabel)    
                    self.central_corner_coordinate.add_widget(self.corner_x)
                    self.central_corner_coordinate.add_widget(self.wallRScoord[oper.number(Parent_name) + oper.number(Select_name) + 'x_corn'])
                    self.central_corner_coordinate.add_widget(Label(text = self.geomspinner.text))
                    self.central_corner_coordinate.add_widget(self.corner_y)
                    self.central_corner_coordinate.add_widget(self.wallRScoord[oper.number(Parent_name) + oper.number(Select_name) + 'y_corn'])
                    self.central_corner_coordinate.add_widget(Label(text = self.geomspinner.text))
                    self.central_window_body.add_widget(self.central_corner_coordinate)
                    self.central_window_body.add_widget(self.size)
                    self.central_size_value.add_widget(self.size_width)
                    self.central_size_value.add_widget(self.wallRScoord[oper.number(Parent_name) + oper.number(Select_name) + 'Widht'])
                    self.central_size_value.add_widget(Label(text = self.geomspinner.text))
                    self.central_size_value.add_widget(self.size_height)
                    self.central_size_value.add_widget(self.wallRScoord[oper.number(Parent_name) + oper.number(Select_name) + 'Hight'])
                    self.central_size_value.add_widget(Label(text = self.geomspinner.text))
                    self.central_size_value.add_widget(Label(text = 'Area:'))
                    self.central_size_value.add_widget(self.wallRScoord[oper.number(Parent_name) + oper.number(Select_name) + 'Area'])
                    self.central_size_value.add_widget(Label(text = self.geomspinner.text + '²'))
                    self.central_window_body.add_widget(self.central_size_value)
                    self.central_window_body.add_widget(Label(text = ''))
                    self.central_window_body.add_widget(self.parlabel)
                    self.central_window_phys_par.add_widget(self.labelEps)
                    self.central_window_phys_par.add_widget(self.wallRSpar[oper.number(Parent_name)  + oper.number(Select_name)  + 'Eps'])
                    self.central_window_phys_par.add_widget(self.unitEps)
                    self.central_window_phys_par.add_widget(self.labelTRS)
                    self.central_window_phys_par.add_widget(self.wallRSpar[oper.number(Parent_name) + oper.number(Select_name) + 'TRS'])
                    self.central_window_phys_par.add_widget(Label(text = self.tempspinner.text))
                    self.central_window_body.add_widget(self.central_window_phys_par)
                    self.up.add_widget(Label(text = 'Ceiling'))
                    if self.RH == '':
                        self.left.add_widget(Label(text = 'Wall ' + str(wall_list[int(oper.number(Parent_name)) - 2])  + ' (Height)'))
                    else:
                        self.left.add_widget(Label(text = 'Wall ' + str(wall_list[int(oper.number(Parent_name)) - 2])  + ' (Height = ' + self.RH +' ' + self.geomspinner.text + ')'))
                    if oper.number(Parent_name) == '4':
                        self.right.add_widget(Label(text = 'Wall 1'))
                    else:
                        self.right.add_widget(Label(text = 'Wall ' + str(wall_list[int(oper.number(Parent_name))])))
                    if (int(oper.number(Parent_name))%2 != 0):
                        if self.RL == '':
                            self.down.add_widget(Label(text = 'Floor (Width)'))
                        else:
                            self.down.add_widget(Label(text = 'Floor (Width = ' + self.RL + ' ' + self.geomspinner.text + ')'))
                    else:
                        if self.RW == '':
                            self.down.add_widget(Label(text = 'Floor (Width)'))
                        else:
                            self.down.add_widget(Label(text = 'Floor (Width = ' + self.RW + ' ' + self.geomspinner.text + ')'))
                    self.graph = GraphBoxLayout()
                    self.central_graph.add_widget(self.graph)

                if ('Floor' in Parent_name) == True:
                    self.central_window_body.add_widget(self.floorRSlabel['FloorRS' + oper.number(Select_name)])                   
                    self.central_window_body.add_widget(self.LeftCornerLabel)    
                    self.central_corner_coordinate.add_widget(self.corner_x)
                    self.central_corner_coordinate.add_widget(self.floorRScoord['FloorRS' + oper.number(Select_name) + 'x_corn'])
                    self.central_corner_coordinate.add_widget(Label(text = self.geomspinner.text))
                    self.central_corner_coordinate.add_widget(self.corner_y)
                    self.central_corner_coordinate.add_widget(self.floorRScoord['FloorRS' + oper.number(Select_name) + 'y_corn'] )
                    self.central_corner_coordinate.add_widget(Label(text = self.geomspinner.text))
                    self.central_window_body.add_widget(self.central_corner_coordinate)
                    self.central_window_body.add_widget(self.size)
                    self.central_size_value.add_widget(self.size_width)
                    self.central_size_value.add_widget(self.floorRScoord['FloorRS' + oper.number(Select_name) + 'Widht'])
                    self.central_size_value.add_widget(Label(text = self.geomspinner.text))
                    self.central_size_value.add_widget(self.size_length)
                    self.central_size_value.add_widget(self.floorRScoord['FloorRS' + oper.number(Select_name) + 'Length'])
                    self.central_size_value.add_widget(Label(text = self.geomspinner.text))
                    self.central_size_value.add_widget(Label(text = 'Area:'))
                    self.central_size_value.add_widget(self.floorRScoord['FloorRS' + oper.number(Select_name) + 'Area'])
                    self.central_size_value.add_widget(Label(text = self.geomspinner.text + '²'))
                    self.central_window_body.add_widget(self.central_size_value)
                    self.central_window_body.add_widget(Label(text = ''))
                    self.central_window_body.add_widget(self.parlabel)
                    self.central_window_phys_par.add_widget(self.labelEps)
                    self.central_window_phys_par.add_widget(self.floorRSpar['FloorRS' + oper.number(Select_name) + 'Eps'])
                    self.central_window_phys_par.add_widget(self.unitEps)
                    self.central_window_phys_par.add_widget(self.labelTRS)
                    self.central_window_phys_par.add_widget(self.floorRSpar['FloorRS' + oper.number(Select_name) + 'TRS'])
                    self.central_window_phys_par.add_widget(Label(text = self.tempspinner.text))
                    self.central_window_body.add_widget(self.central_window_phys_par)
                    
                    self.up.add_widget(Label(text = 'Wall 2'))
                    if self.RL != '':
                        self.left.add_widget(Label(text = 'Wall 1 (Length = ' + self.RL + ' ' + self.geomspinner.text + ')'))
                    else:
                        self.left.add_widget(Label(text = 'Wall 1 (Length)'))
                    self.right.add_widget(Label(text = 'Wall 3'))
                    if self.RW != '':
                        self.down.add_widget(Label(text = 'Wall 4 (Width = ' + self.RW + ' ' + self.geomspinner.text + ')'))
                    else:
                        self.down.add_widget(Label(text = 'Wall 4 (Width)'))
                    self.graph = GraphBoxLayout()
                    self.central_graph.add_widget(self.graph)
                if ('Ceiling' in Parent_name) == True:
                    self.central_window_body.add_widget(self.ceilingRSlabel['CeilingRS' + oper.number(Select_name)])                   
                    self.central_window_body.add_widget(self.LeftCornerLabel)    
                    self.central_corner_coordinate.add_widget(self.corner_x)
                    self.central_corner_coordinate.add_widget(self.ceilingRScoord['CeilingRS' + oper.number(Select_name) + 'x_corn'])
                    self.central_corner_coordinate.add_widget(Label(text = self.geomspinner.text))
                    self.central_corner_coordinate.add_widget(self.corner_y)
                    self.central_corner_coordinate.add_widget(self.ceilingRScoord['CeilingRS' + oper.number(Select_name) + 'y_corn'] )
                    self.central_corner_coordinate.add_widget(Label(text = self.geomspinner.text))
                    self.central_window_body.add_widget(self.central_corner_coordinate)
                    self.central_window_body.add_widget(self.size)
                    self.central_size_value.add_widget(self.size_width)
                    self.central_size_value.add_widget(self.ceilingRScoord['CeilingRS' + oper.number(Select_name) + 'Widht'])
                    self.central_size_value.add_widget(Label(text = self.geomspinner.text))
                    self.central_size_value.add_widget(self.size_length)
                    self.central_size_value.add_widget(self.ceilingRScoord['CeilingRS' + oper.number(Select_name) + 'Length'])
                    self.central_size_value.add_widget(Label(text = self.geomspinner.text))
                    self.central_size_value.add_widget(Label(text = 'Area:'))
                    self.central_size_value.add_widget(self.ceilingRScoord['CeilingRS' + oper.number(Select_name) + 'Area'])
                    self.central_size_value.add_widget(Label(text = self.geomspinner.text + '²'))
                    self.central_window_body.add_widget(self.central_size_value)
                    self.central_window_body.add_widget(Label(text = ''))
                    self.central_window_body.add_widget(self.parlabel)
                    self.central_window_phys_par.add_widget(self.labelEps)
                    self.central_window_phys_par.add_widget(self.ceilingRSpar['CeilingRS' + oper.number(Select_name) + 'Eps'])
                    self.central_window_phys_par.add_widget(self.unitEps)
                    self.central_window_phys_par.add_widget(self.labelTRS)
                    self.central_window_phys_par.add_widget(self.ceilingRSpar['CeilingRS' + oper.number(Select_name) + 'TRS'])
                    self.central_window_phys_par.add_widget(Label(text = self.tempspinner.text))
                    self.central_window_body.add_widget(self.central_window_phys_par)                   
                    self.up.add_widget(Label(text = 'Wall 2'))
                    if self.RL != '':
                        self.left.add_widget(Label(text = 'Wall 1 (Length = ' + self.RL + ' ' + self.geomspinner.text + ')'))
                    else:
                        self.left.add_widget(Label(text = 'Wall 1 (Length)'))
                    self.right.add_widget(Label(text = 'Wall 3'))
                    if self.RW != '':
                        self.down.add_widget(Label(text = 'Wall 4 (Width = ' + self.RW + ' ' + self.geomspinner.text + ')'))
                    else:
                        self.down.add_widget(Label(text = 'Wall 4 (Width)'))                    
                    self.graph = GraphBoxLayout()
                    self.central_graph.add_widget(self.graph)

            if ('Window/Door' in Select_name) == True:
                wall_list = [1,2,3,4]
                Parent_name = self.model_tree.selected_node.parent_node.text
                self.central_window_body.add_widget(self.wallOplabel[oper.number(Parent_name) + oper.number(Select_name)])
                
                self.central_window_body.add_widget(self.LeftCornerLabel)    
                self.central_corner_coordinate.add_widget(self.corner_x)
                self.central_corner_coordinate.add_widget(self.wallOpcoord[oper.number(Parent_name) + oper.number(Select_name) + 'x_corn'])
                self.central_corner_coordinate.add_widget(Label(text = self.geomspinner.text))
                self.central_corner_coordinate.add_widget(self.corner_y)
                self.central_corner_coordinate.add_widget(self.wallOpcoord[oper.number(Parent_name) + oper.number(Select_name) + 'y_corn'])
                self.central_corner_coordinate.add_widget(Label(text = self.geomspinner.text))
                self.central_window_body.add_widget(self.central_corner_coordinate)
                self.central_window_body.add_widget(self.size)
                self.central_size_value.add_widget(self.size_width)
                self.central_size_value.add_widget(self.wallOpcoord[oper.number(Parent_name) + oper.number(Select_name) + 'Widht'])
                self.central_size_value.add_widget(Label(text = self.geomspinner.text))
                self.central_size_value.add_widget(self.size_height)
                self.central_size_value.add_widget(self.wallOpcoord[oper.number(Parent_name) + oper.number(Select_name) + 'Hight'])
                self.central_size_value.add_widget(Label(text = self.geomspinner.text))
                self.central_size_value.add_widget(Label(text = 'Area:'))
                self.central_size_value.add_widget(self.wallOpcoord[oper.number(Parent_name) + oper.number(Select_name) + 'Area'])
                self.central_size_value.add_widget(Label(text = self.geomspinner.text + '²'))
                self.central_window_body.add_widget(self.central_size_value)
                self.central_window_body.add_widget(Label(text = ''))
                self.central_window_body.add_widget(self.parlabel)
                self.central_window_phys_par.add_widget(self.labelEps)
                self.central_window_phys_par.add_widget(self.wallOppar[oper.number(Parent_name)  + oper.number(Select_name)  + 'Eps'])
                self.central_window_phys_par.add_widget(self.unitEps)
                self.central_window_phys_par.add_widget(self.labelU)
                self.central_window_phys_par.add_widget(self.wallOppar[oper.number(Parent_name)  + oper.number(Select_name)  + 'U'])
                self.central_window_phys_par.add_widget(self.unitU)
                self.central_window_phys_par.add_widget(self.labelTex)
                self.central_window_phys_par.add_widget(Label(text = self.WallParInput['Tex' + oper.number(Parent_name)].text, size_hint_x=None, width=100))
                self.central_window_phys_par.add_widget(Label(text = self.tempspinner.text))
                self.central_window_body.add_widget(self.central_window_phys_par)    
                self.up.add_widget(Label(text = 'Ceiling'))
                if self.RH == '':
                    self.left.add_widget(Label(text = 'Wall ' + str(wall_list[int(oper.number(Parent_name)) - 2])  + ' (Height)'))
                else:
                    self.left.add_widget(Label(text = 'Wall ' + str(wall_list[int(oper.number(Parent_name)) - 2])  + ' (Height = ' + self.RH + ' ' + self.geomspinner.text + ')'))
                if oper.number(Parent_name) == '4':
                    self.right.add_widget(Label(text = 'Wall 1'))
                else:
                    self.right.add_widget(Label(text = 'Wall ' + str(wall_list[int(oper.number(Parent_name))])))
                if (int(oper.number(Parent_name))%2 != 0):
                    if self.RL == '':
                        self.down.add_widget(Label(text = 'Floor (Width)'))
                    else:
                        self.down.add_widget(Label(text = 'Floor (Width = ' + self.RL + ' ' + self.geomspinner.text + ')'))
                else:
                    if self.RW == '':
                        self.down.add_widget(Label(text = 'Floor (Width)'))
                    else:
                        self.down.add_widget(Label(text = 'Floor (Width = ' + self.RW + ' ' + self.geomspinner.text + ')'))
                self.graph = GraphBoxLayout()
                self.central_graph.add_widget(self.graph)

    #User parameteres collecting
    def calculate(self, *args):

        self.resultclick += 1
        self.right_window_results_data_layout.clear_widgets()
        #Calculation
        self.time.clear_widgets()
        self.Calcresult = 0
        #Calculation
        try:
            self.Calcresult = calc.calculation(cd.collect(self, *args))
        except ValueError:
            self.time.add_widget(Label (text = 'Set all data in options'))
            return()
        self.CopyCalcresult = ''
        for key in self.Calcresult:
            self.CopyCalcresult += key + ' ' + str(self.Calcresult[key]) + '\n'
        self.time.add_widget(Label (text = 'Last calculation time: ' + self.Calcresult['Solution time'] + ' sec'))
        #Results demonstration after press "Calculate"
        if self.resultclick > 0:
            self.right_window_results_data_layout.clear_widgets()
            self.right_window_results_data = GridLayout(cols = 3, row_force_default = True, row_default_height = 30)
            self.right_window_results_data_layout.add_widget(self.right_window_results_data)
            self.right_window_results_data.clear_widgets()
            self.right_window_results_data.add_widget(Label(text = 'Structure'))
            self.right_window_results_data.add_widget(Label(text = 'Outer temperatures, °C'))
            self.right_window_results_data.add_widget(Label(text = 'Inner temperatures, °C'))
            for key in self.Calcresult['Temperatures']:
                if ('Window' in key) == True:
                    self.right_window_results_data.add_widget(TextInput(text = '    ' + key))
                else:
                    self.right_window_results_data.add_widget(TextInput(text = key))
                self.right_window_results_data.add_widget(TextInput(text = str(self.Calcresult['TemperaturesOut'][key]))) 
                self.right_window_results_data.add_widget(TextInput(text = str(self.Calcresult['Temperatures'][key])))
        return(self.Calcresult)
        
    def copyresult(self, *args):   
        if len(self.CopyCalcresult) != 0:
            Clipboard.copy(self.CopyCalcresult)
        else:
            pass

    def tempresults(self, *args):
        if (self.resultclick > 0) and (self.Calcresult != 0):
            self.right_window_results_data_layout.clear_widgets()
            self.right_window_results_data = GridLayout(cols = 3, row_force_default = True, row_default_height = 30)
            self.right_window_results_data_layout.add_widget(self.right_window_results_data)
            self.right_window_results_data.clear_widgets()
            self.right_window_results_data.add_widget(Label(text = 'Structure'))
            self.right_window_results_data.add_widget(Label(text = 'Outer temperatures, °C'))
            self.right_window_results_data.add_widget(Label(text = 'Inner temperatures, °C'))
            for key in self.Calcresult['Temperatures']:
                if ('Window' in key) == True:
                    self.right_window_results_data.add_widget(TextInput(text = '    ' + key))
                else:
                    self.right_window_results_data.add_widget(TextInput(text = key))
                self.right_window_results_data.add_widget(TextInput(text = str(self.Calcresult['TemperaturesOut'][key]))) 
                self.right_window_results_data.add_widget(TextInput(text = str(self.Calcresult['Temperatures'][key])))


    def hbresults(self, *args):
        if (self.resultclick > 0) and (self.Calcresult != 0):
            self.right_window_results_data_layout.clear_widgets()
            self.right_window_results_data = GridLayout(cols = 4, row_force_default = True, row_default_height = 30)
            self.right_window_results_data_layout.add_widget(self.right_window_results_data)
            self.right_window_results_data.clear_widgets()
            self.right_window_results_data.add_widget(Label(text = 'Structure'))
            self.right_window_results_data.add_widget(Label(text = 'Source flux, W/m²'))
            self.right_window_results_data.add_widget(Label(text = 'Power source, W'))
            self.right_window_results_data.add_widget(Label(text = 'Power losse, W'))           
            for key in self.Calcresult['Heat']['Heat power']:
                if ('Window' in key) == True:
                    self.right_window_results_data.add_widget(TextInput(text = '    ' + key))
                else:
                    self.right_window_results_data.add_widget(TextInput(text = key))
                self.right_window_results_data.add_widget(TextInput(text = str(self.Calcresult['Heat']['Heat flux'][key])))
                self.right_window_results_data.add_widget(TextInput(text = str(self.Calcresult['Heat']['Heat power'][key])))
                self.right_window_results_data.add_widget(TextInput(text = str(self.Calcresult['Losses'][key])))
               
    def Build(self, *args):
        try:
            Parent_name = self.model_tree.selected_node.parent_node.text
            self.graph.canvas.clear()
            Select_name = self.model_tree.selected_node.text
        except AttributeError:
            return()
        try:
            
            if ('Ceiling' in Parent_name) == True:
                for i in range(len(self.ceilingRSdata)):
                    self.X_coord = float(self.ceilingRScoord['CeilingRS' + self.ceilingRSdata[i] + 'x_corn'].text) * (self.central_graph.width) / float(self.Room['RW'].text)
                    self.Y_coord = float(self.ceilingRScoord['CeilingRS' + self.ceilingRSdata[i] + 'y_corn'].text) * (self.central_graph.height ) / float(self.Room['RL'].text)
                    self.W_coord = float(self.ceilingRScoord['CeilingRS' + self.ceilingRSdata[i] + 'Widht'].text) * (self.central_graph.width ) / float(self.Room['RW'].text)
                    self.L_coord = float(self.ceilingRScoord['CeilingRS' + self.ceilingRSdata[i] + 'Length'].text) * (self.central_graph.height) / float(self.Room['RL'].text)
                    with self.graph.canvas:
                        Color(rgba=(.5, 0, 0, 1))
                        self.bg = Rectangle(pos=(self.central_graph.x + self.X_coord, self.central_graph.y + self.Y_coord), size=(self.W_coord, self.L_coord))
                area = float(self.ceilingRScoord['CeilingRS' + oper.number(Select_name) + 'Widht'].text) * float(self.ceilingRScoord['CeilingRS' + oper.number(Select_name) + 'Length'].text)
                self.ceilingRScoord['CeilingRS' + oper.number(Select_name) + 'Area'].text = str(round(area, 1)) 
            if ('Floor' in Parent_name) == True:
                for i in range(len(self.floorRSdata)):
                    self.X_coord = float(self.floorRScoord['FloorRS' + self.floorRSdata[i] + 'x_corn'].text) * (self.central_graph.width) / float(self.Room['RW'].text)
                    self.Y_coord = float(self.floorRScoord['FloorRS' + self.floorRSdata[i] + 'y_corn'].text) * (self.central_graph.height ) / float(self.Room['RL'].text)
                    self.W_coord = float(self.floorRScoord['FloorRS' + self.floorRSdata[i] + 'Widht'].text) * (self.central_graph.width ) / float(self.Room['RW'].text)
                    self.L_coord = float(self.floorRScoord['FloorRS' + self.floorRSdata[i] + 'Length'].text) * (self.central_graph.height) / float(self.Room['RL'].text)
                    with self.graph.canvas:
                        Color(rgba=(.5, 0, 0, 1))
                        self.bg = Rectangle(pos=(self.central_graph.x + self.X_coord, self.central_graph.y + self.Y_coord), size=(self.W_coord, self.L_coord))
                area = float(self.floorRScoord['FloorRS' + oper.number(Select_name) + 'Widht'].text) * float(self.floorRScoord['FloorRS' + oper.number(Select_name) + 'Length'].text)
                self.floorRScoord['FloorRS' + oper.number(Select_name) + 'Area'].text = str(round(area, 1))                  
            if ('Wall' in Parent_name) == True:
                R = 0
                if (int(oper.number(Parent_name))%2 == 0):
                    R = 'RW'
                else: 
                    R = 'RL'
                wn = int(oper.number(Parent_name)) - 1
                for j in range(len(self.wallRSdata[wn])):                       
                    self.X_coord = float(self.wallRScoord[self.wallRSdata[wn][j] + 'x_corn'].text) * (self.central_graph.width) / float(self.Room[R].text)
                    self.Y_coord = float(self.wallRScoord[self.wallRSdata[wn][j] + 'y_corn'].text) * (self.central_graph.height ) / float(self.Room['RH'].text)
                    self.W_coord = float(self.wallRScoord[self.wallRSdata[wn][j] + 'Widht'].text) * (self.central_graph.width ) / float(self.Room[R].text)
                    self.L_coord = float(self.wallRScoord[self.wallRSdata[wn][j] + 'Hight'].text) * (self.central_graph.height) / float(self.Room['RH'].text)
                    with self.graph.canvas:
                        Color(rgba=(.5, 0, 0, 1))
                        self.bg = Rectangle(pos=(self.central_graph.x + self.X_coord, self.central_graph.y + self.Y_coord), size=(self.W_coord, self.L_coord))
                for k in range(len(self.wallOpdata[wn])):     
                    self.X_coord = float(self.wallOpcoord[self.wallOpdata[wn][k] + 'x_corn'].text) * (self.central_graph.width) / float(self.Room[R].text)
                    self.Y_coord = float(self.wallOpcoord[self.wallOpdata[wn][k] + 'y_corn'].text) * (self.central_graph.height ) / float(self.Room['RH'].text)
                    self.W_coord = float(self.wallOpcoord[self.wallOpdata[wn][k] + 'Widht'].text) * (self.central_graph.width ) / float(self.Room[R].text)
                    self.L_coord = float(self.wallOpcoord[self.wallOpdata[wn][k] + 'Hight'].text) * (self.central_graph.height) / float(self.Room['RH'].text)
                    with self.graph.canvas:
                        Color(rgba=(0, 0, .5, 1))
                        self.bg = Rectangle(pos=(self.central_graph.x + self.X_coord, self.central_graph.y + self.Y_coord), size=(self.W_coord, self.L_coord))
                if ('Radiant' in Select_name) == True:
                    area = (float(self.wallRScoord[oper.number(Parent_name) + oper.number(Select_name) + 'Widht'].text) * float(self.wallRScoord[oper.number(Parent_name) + oper.number(Select_name) + 'Hight'].text))
                    self.wallRScoord[oper.number(Parent_name) + oper.number(Select_name) + 'Area'].text = str(round(area, 1))
                if ('Window' in Select_name) == True:
                    area = (float(self.wallOpcoord[oper.number(Parent_name) + oper.number(Select_name) + 'Widht'].text) * float(self.wallOpcoord[oper.number(Parent_name) + oper.number(Select_name) + 'Hight'].text))
                    self.wallOpcoord[oper.number(Parent_name) + oper.number(Select_name) + 'Area'].text = str(round(area, 1))
        except ValueError:
            return()       

    def room_resize(self, *args):
        self.RW = self.Room['RW'].text
        self.RL = self.Room['RL'].text
        self.RH = self.Room['RH'].text
        if self.RL != '':
            self.leftlabel.text = 'Wall 1 (Length = ' + self.RL + ' ' + self.geomspinner.text + ')'
        if self.RW != '':
            self.rightlabel.text = 'Wall 4 (Width = ' + self.RW + ' ' + self.geomspinner.text + ')'

    def build(self):
        root = MyFloatLayout()       
        root.add_widget(self.base_layer)
        return root

if __name__ == '__main__':
    RHCApp().run()