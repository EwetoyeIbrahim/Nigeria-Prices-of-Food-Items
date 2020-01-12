'''
It consist of universal functions such as:
dashboard_template: for contructing the public dashboard template
'''
import os
from functools import reduce
from random import randrange

ads_val = {
    0:'''
    <img class="img-responsive center-block hidden-sm hidden-xs" src="../shared_res/ads0.jpg" alt="ads">
    <img class="img-responsive center-block hidden-md hidden-lg" src="../shared_res/ads1.jpg" alt="ads">
    ''',
    1:'''
    <a class="hidden-sm hidden-xs" href="https://c.jumia.io/?a=147346&c=1613&p=r&E=kkYNyk2M4sk%3D&utm_campaign=147346&utm_term=" target="_blank"><img class="img-responsive center-block" src="assets/JumiaCompute300_600.jpeg"/></a>
    <a class="hidden-md hidden-lg" href="https://c.jumia.io/?a=147346&c=1613&p=r&E=kkYNyk2M4sk%3D&utm_campaign=147346&utm_term=" target="_blank"><img class="img-responsive center-block" src="assets/JumiaCompute970_90.jpeg"/></a>
    ''',
}

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
    
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'public_dashboard.html')) as f:
        template_html = f.read()
    template_vars = {"page_title": page_title,"page_subtitle":page_subtitle,
                     "author_name": author_name,
                     "header_img_path": header_img_path,"header_img_alt":header_img_alt,
                     "links_to_related_files": links_to_related_files,
                     "generated_advert":generated_advert,"list_of_recent_visuals":list_of_recent_visuals,
                     # I am doing -1 of advert length because I am disabling Jumia for now
                     "sidebar_content":sidebar_content, "ads_area":ads_val[randrange(len(ads_val)-1)],}
    
    index_string = reduce(lambda p, q: p.replace(*q), template_vars.items(), template_html)
    return index_string
