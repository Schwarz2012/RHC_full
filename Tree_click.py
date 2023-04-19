def delete(self, *obj):      
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
            if ('Opening' in Select_name) == True:
                    Parent_name = self.model_tree.selected_node.parent_node.text
                    self.wallOpdata[int(oper.number(Parent_name))-1].remove(oper.number(Parent_name) + oper.number(Select_name))
                    self.model_tree.remove_node(self.model_tree.selected_node)
                    self.central_window_body.clear_widgets()