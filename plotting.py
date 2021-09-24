from motion_detector import df 
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource

df['Start_String']= df['Start'].dt.strftime('%Y-%m-%d %H:%M:%S')
df['End_String']= df['End'].dt.strftime('%Y-%m-%d %H:%M:%S')

cds= ColumnDataSource(df)

output_file('Web_Cam_Plotting.html')

f=figure(plot_width = 1200, plot_height = 300, x_axis_type= 'datetime', title= 'Motion Graph', sizing_mode="stretch_width")
f.yaxis.minor_tick_line_color=None
f.yaxis.ticker.desired_num_ticks = 1

hover= HoverTool(tooltips= [('Start Time', '@Start_String'), ('End Time', '@End_String')])
f.add_tools(hover)

q=f.quad(top=0, bottom=1, left='Start', right='End', color="green", source=cds)
show(f)