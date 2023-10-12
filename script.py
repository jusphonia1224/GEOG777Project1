import arcpy
from arcpy import env
from arcpy.sa import *
import arcgis

import wx
import wx.xrc


# Set environment settings
env.workspace = "D:/GEOG777/Project"
arcpy.env.overwriteOutput = True

# Open project
project_path = "D:/GEOG777/Project/Project/Project1.aprx"
aprx = arcpy.mp.ArcGISProject(project_path)
map = aprx.listMaps()[0]
layout = aprx.listLayouts()[0]

text_element_name = "TextMapTitle"

# Find the map title element by its name
text_element_to_change = None
for element in layout.listElements():
    if element.name == text_element_name:
        text_element_to_change = element
        break

# Datasets
nitrate = env.workspace + "/Project1DB.gdb/well_nitrate"
cancer = env.workspace + "/Project1DB.gdb/cancer_tracts"

# Generate default image
map_left_blank = env.workspace + "/Project1DB.gdb/left_blank.png"
nitrate_layer = map.addDataFromPath(nitrate)
# Set the path to the layer file with the desired symbology
symbology_layer_path = "D:/GEOG777/Project/Project/nitrate_symbol.lyrx"
# Apply the symbology from the symbology layer to the layer
arcpy.ApplySymbologyFromLayer_management(nitrate_layer, symbology_layer_path)
# Change the text of the map title
if text_element_to_change:
    text_element_to_change.text = "Nitrate Level"
# Export map to png
layout.exportToPNG(map_left_blank)
map.removeLayer(nitrate_layer)

map_right_blank = env.workspace + "/Project1DB.gdb/right_blank.png"
cancer_layer = map.addDataFromPath(cancer)
# Set the path to the layer file with the desired symbology
symbology_layer_path = "D:/GEOG777/Project/Project/cancer_symbol.lyrx"
# Apply the symbology from the symbology layer to the layer
arcpy.ApplySymbologyFromLayer_management(cancer_layer, symbology_layer_path)

# Change the text of the map title
if text_element_to_change:
    text_element_to_change.text = "Cancer Rate"
# Export map to png
layout.exportToPNG(map_right_blank)
map.removeLayer(cancer_layer)


###########################################################################
## GUI
###########################################################################
class LeftMapPanel(wx.Panel):
    def __init__(self, parent):
        super(LeftMapPanel, self).__init__(parent)

        # Load the map image
        map_left_image = wx.Image(map_left_blank, wx.BITMAP_TYPE_PNG)
        self.map_left_bitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(map_left_image))

        # Create a vertical box sizer for the map panel
        bSizerMapLeft = wx.BoxSizer(wx.VERTICAL)
        bSizerMapLeft.Add(self.map_left_bitmap, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizerMapLeft)

    def update_map(self, map_image_path):
        # Load the new map image
        map_image = wx.Image(map_image_path, wx.BITMAP_TYPE_ANY)
        # Update the static bitmap with the new map image
        self.map_left_bitmap.SetBitmap(wx.Bitmap(map_image))
        self.Refresh()

class RightMapPanel(wx.Panel):
    def __init__(self, parent):
        super(RightMapPanel, self).__init__(parent)

        # Load the map image
        map_right_image = wx.Image(map_right_blank, wx.BITMAP_TYPE_PNG)
        self.map_right_bitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(map_right_image))

        # Create a vertical box sizer for the map panel
        bSizerMapRight = wx.BoxSizer(wx.VERTICAL)
        bSizerMapRight.Add(self.map_right_bitmap, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizerMapRight)

    def update_map(self, map_image_path):
        # Load the new map image
        map_image = wx.Image(map_image_path, wx.BITMAP_TYPE_ANY)
        # Update the static bitmap with the new map image
        self.map_right_bitmap.SetBitmap(wx.Bitmap(map_image))
        self.Refresh()

class GUI ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1000,610 ), style = 0|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizerOverall = wx.BoxSizer( wx.VERTICAL )

        gbSizerUpper = wx.GridBagSizer( 0, 0 )
        gbSizerUpper.SetFlexibleDirection( wx.BOTH )
        gbSizerUpper.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_ALL )

        self.labelDecay = wx.StaticText( self, wx.ID_ANY, u"Decay coefficient k:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.labelDecay.Wrap( -1 )

        gbSizerUpper.Add( self.labelDecay, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.textboxDecay = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizerUpper.Add( self.textboxDecay, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.buttonRun = wx.Button( self, wx.ID_ANY, u"Run", wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizerUpper.Add( self.buttonRun, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.buttonReset = wx.Button( self, wx.ID_ANY, u"Reset", wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizerUpper.Add( self.buttonReset, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        #self.buttonExit = wx.Button( self, wx.ID_ANY, u"X", wx.DefaultPosition, wx.Size( 20,20 ), 0 )
        self.buttonExit = wx.Button( self, wx.ID_ANY, u"Close Program", wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizerUpper.Add( self.buttonExit, wx.GBPosition( 0, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.labelStatus = wx.StaticText( self, wx.ID_ANY, u"Waiting Input", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.labelStatus.Wrap( -1 )
        gbSizerUpper.Add( self.labelStatus, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        bSizerOverall.Add( gbSizerUpper, 1, wx.EXPAND|wx.TOP, 5 )

        gSizerLower = wx.GridSizer( 0, 2, 0, 0 )

        self.m_panelLeft = LeftMapPanel(self)
        bSizerLeft = wx.BoxSizer(wx.VERTICAL)

        self.m_panelLeft.SetSizer(bSizerLeft)
        self.m_panelLeft.Layout()
        bSizerLeft.Fit(self.m_panelLeft)
        gSizerLower.Add(self.m_panelLeft, 1, wx.EXPAND | wx.ALL, 5)

        self.m_panelRight = RightMapPanel(self)
        bSizerRight = wx.BoxSizer( wx.VERTICAL )

        self.m_panelRight.SetSizer( bSizerRight )
        self.m_panelRight.Layout()
        bSizerRight.Fit( self.m_panelRight )
        gSizerLower.Add( self.m_panelRight, 1, wx.EXPAND |wx.ALL, 5 )


        bSizerOverall.Add( gSizerLower, 7, wx.EXPAND, 5 )


        self.SetSizer( bSizerOverall )
        self.Layout()

        self.Centre( wx.BOTH )

        # Events
        self.buttonExit.Bind(wx.EVT_BUTTON, self.onClickExit)
        self.buttonRun.Bind(wx.EVT_BUTTON, self.onClickRun)
        self.buttonReset.Bind(wx.EVT_BUTTON, self.onClickReset)


    def onClickExit(self, event):
        self.Close()
        self.Destroy()

    def onClickReset(self, event):
        self.m_panelLeft.update_map(map_left_blank)
        self.m_panelRight.update_map(map_right_blank)
        self.textboxDecay.Clear()

    ###########################################################################
    ## Spatial Analysis
    ###########################################################################
    def onClickRun(self, event):
        self.labelStatus.SetLabel("Processing Interpolation")
        paramK = self.textboxDecay.GetValue()

        # Dataset
        nitrate_cancer = "Project1DB.gdb/nitrate_cancer"

        # Set local variables
        inPointFeatures = nitrate
        zField = "nitr_ran"
        cellSize = 0.017616319278512
        power = paramK #2
        searchRadius = RadiusFixed(0.2,)

        # Execute IDW
        outIDW = Idw(nitrate, zField, cellSize, power, searchRadius)

        # Save the output
        outIDW_path = env.workspace + "/Project1DB.gdb/IDW_Raster1"
        outIDW.save(outIDW_path)

        # Display on IDW
        idw_layer = map.addDataFromPath(outIDW_path)

        # Set the path to the layer file with the desired symbology
        symbology_layer_path = "D:/GEOG777/Project/Project/idw_symbol.lyrx"

        # Apply the symbology from the symbology layer to the layer
        arcpy.ApplySymbologyFromLayer_management(idw_layer, symbology_layer_path)

        map_export_path = env.workspace + "/Project1DB.gdb/IDW.png"
        # Change the text of the map title
        if text_element_to_change:
            text_element_to_change.text = "IDW with distance " + paramK
        # Export map to png
        layout.exportToPNG(map_export_path)

        self.m_panelLeft.update_map(map_export_path)
        map.removeLayer(idw_layer)

        # Execute Linear Regression
        self.labelStatus.SetLabel("Processing Regression")
        outLR = env.workspace + "/Project1DB.gdb/nitrate_cancer_GLR"
        arcpy.stats.GeneralizedLinearRegression(nitrate_cancer, "MEAN_nitr_ran", "CONTINUOUS", outLR, ["canrate"], "", "", "", "")

        # Export active map as an image
        regression_layer = map.addDataFromPath(outLR)
        map_export_path = env.workspace + "/Project1DB.gdb/GLR.png"
        # Change the text of the map title
        if text_element_to_change:
            text_element_to_change.text = "Regression on Nitrate-Cancer"
        # Export map to png
        layout.exportToPNG(map_export_path)

        self.m_panelRight.update_map(map_export_path)
        map.removeLayer(regression_layer)

        self.labelStatus.SetLabel("Completed")


    def __del__( self ):
        pass

if __name__ == '__main__':
    # Call UI
    app = wx.App()

    # Create a wx.Locale object to set the desired locale
    locale = wx.Locale(wx.LANGUAGE_DEFAULT)

    gui_frame = GUI(None)
    gui_frame.Show(True)
    app.MainLoop()