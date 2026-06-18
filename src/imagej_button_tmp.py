import imagej
import scyjava

# Start ImageJ with UI
ij = imagej.init(mode='interactive', add_legacy=True)
ij.ui().showUI()
# Import Java Swing classes
JButton = scyjava.jimport('javax.swing.JButton')
JFrame = scyjava.jimport('javax.swing.JFrame')

# Define a Python callback
def on_click(event):
    print("Button clicked! Running Python code...")
    # Put your Python logic here

# Create the button
button = JButton("Run Python")
button.addActionListener(on_click)

# Create a window to hold it
frame = JFrame("Python-Controlled Button")
frame.add(button)
frame.pack()
frame.setVisible(True)

# import os
# import imagej
# import scyjava

# # Force ImageJ2 Swing UI (prevents Legacy UI from taking over)
# #os.environ["scijava.ui"] = "org.scijava.ui.swing.SwingUI"

# # IMPORTANT: point this to your Fiji installation
# ij = imagej.init(mode='interactive', add_legacy=True)

# # Show the ImageJ UI
# ij.ui().showUI()

# # Import Java Swing classes
# JPanel = scyjava.jimport('javax.swing.JPanel')
# JButton = scyjava.jimport('javax.swing.JButton')
# BorderLayout = scyjava.jimport('java.awt.BorderLayout')

# # Access ImageJ's UI service
# UIService = scyjava.jimport('org.scijava.ui.UIService')
# ui = ij.getContext().getService(UIService)

# # Python callback
# def on_click(event):
#     print("Button clicked! Running Python code...")

# # Build the dockable panel
# panel = JPanel(BorderLayout())
# button = JButton("Run Python")
# button.addActionListener(on_click)
# panel.add(button, BorderLayout.CENTER)

# # Show as a dockable panel inside ImageJ
# ui.show("Python Tools", panel)

# # Verify which UI is active (should print SwingUI)
# #print("Active UI:", ij.ui().getUI().getClass().getName())


# UIService = scyjava.jimport('org.scijava.ui.UIService')
# ui_service = ij.getContext().getService(UIService)
# active_ui = ui_service.getDefaultUI()
# print("Active UI:", active_ui.getClass().getName())


# #from javax.swing import SwingUtilities

# #SwingUtilities.invokeLater(lambda: None)


# # import imagej
# # import scyjava

# # ij = imagej.init(mode='interactive')

# # JPanel = scyjava.jimport('javax.swing.JPanel')
# # JButton = scyjava.jimport('javax.swing.JButton')
# # BorderLayout = scyjava.jimport('java.awt.BorderLayout')
# # UIService = scyjava.jimport('org.scijava.ui.UIService')

# # ui = ij.getContext().getService(UIService)

# # def on_click(event):
# #     print("Button clicked from inside ImageJ!")

# # panel = JPanel(BorderLayout())
# # button = JButton("Run Python")
# # button.addActionListener(on_click)
# # panel.add(button, BorderLayout.CENTER)

# # ui.show("Python Tools", panel)