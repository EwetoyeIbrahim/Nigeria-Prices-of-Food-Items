'''
It consist of universal functions such as:
dashboard_template: for contructing the public dashboard template
'''
from functools import reduce

def dashboard_template(page_title="DataVisuals",
                         page_subtitle="Visualizing Historical Trend",
                         meta_tag="Visualizing historical data",
                         header_img_path="./images/backgroun1.jpg",
                         header_img_alt="DataVisuals.com",
                         links_to_related_files = "",
                         generated_advert="",
                         list_of_recent_visuals="",
                         sidebar_content = "",
                         author_name = "Ewetoye Ibrahim"
                         ):
    '''
    constructs the public dashboard base templates by substituting the passed parameter
    '''
    with open(r'C:\Users\MEDSAF\Desktop\Apps\VirtualDataWeb\Dashboards\NigeriaFoodPrice\_shared_res\dashtemp.html','r') as f:
        template_html = f.read()
    template_vars = {"page_title": page_title,"page_subtitle":page_subtitle,
                     "author_name": author_name,
                     "header_img_path": header_img_path,"header_img_alt":header_img_alt,
                     "links_to_related_files": links_to_related_files,
                     "generated_advert":generated_advert,"list_of_recent_visuals":list_of_recent_visuals,
                     "sidebar_content":sidebar_content}
    
    index_string = reduce(lambda p, q: p.replace(*q), template_vars.items(), template_html)
    return index_string
