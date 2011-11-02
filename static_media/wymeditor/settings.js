var KAPUA_WYM_SETTINGS = {		
	containersItems: [
	    {'name': 'P', 'title': 'Paragraph', 'css': 'wym_containers_p'},
	    /*{'name': 'H1', 'title': 'Heading_1', 'css': 'wym_containers_h1'},*/
	    {'name': 'H2', 'title': 'Heading_2', 'css': 'wym_containers_h2'},
	    {'name': 'H3', 'title': 'Heading_3', 'css': 'wym_containers_h3'},
	    {'name': 'H4', 'title': 'Heading_4', 'css': 'wym_containers_h4'},
	    {'name': 'H5', 'title': 'Heading_5', 'css': 'wym_containers_h5'},
	    {'name': 'H6', 'title': 'Heading_6', 'css': 'wym_containers_h6'},
	    {'name': 'PRE', 'title': 'Preformatted', 'css': 'wym_containers_pre'},
	    {'name': 'BLOCKQUOTE', 'title': 'Blockquote', 'css': 'wym_containers_blockquote'},
	    {'name': 'TH', 'title': 'Table_Header', 'css': 'wym_containers_th'}
	],
	
	toolsItems: [
	    /*{'name': 'Bold', 'title': 'Strong', 'css': 'wym_tools_strong'},*/
	    /*{'name': 'Italic', 'title': 'Emphasis', 'css': 'wym_tools_emphasis'},*/
	    {'name': 'Superscript', 'title': 'Superscript', 'css': 'wym_tools_superscript'},
	    {'name': 'Subscript', 'title': 'Subscript', 'css': 'wym_tools_subscript'},
	    {'name': 'InsertOrderedList', 'title': 'Ordered_List', 'css': 'wym_tools_ordered_list'},
	    {'name': 'InsertUnorderedList', 'title': 'Unordered_List', 'css': 'wym_tools_unordered_list'},
	    {'name': 'Indent', 'title': 'Indent', 'css': 'wym_tools_indent'},
	    {'name': 'Outdent', 'title': 'Outdent', 'css': 'wym_tools_outdent'},
	    {'name': 'Undo', 'title': 'Undo', 'css': 'wym_tools_undo'},
	    {'name': 'Redo', 'title': 'Redo', 'css': 'wym_tools_redo'},
	    {'name': 'CreateLink', 'title': 'Link', 'css': 'wym_tools_link'},
	    {'name': 'Unlink', 'title': 'Unlink', 'css': 'wym_tools_unlink'},
	    {'name': 'InsertImage', 'title': 'Image', 'css': 'wym_tools_image'},
	    {'name': 'InsertTable', 'title': 'Table', 'css': 'wym_tools_table'},
	    /*{'name': 'Paste', 'title': 'Paste_From_Word', 'css': 'wym_tools_paste'},*/
	    {'name': 'ToggleHtml', 'title': 'HTML', 'css': 'wym_tools_html'},
	    {'name': 'Preview', 'title': 'Preview', 'css': 'wym_tools_preview'}
	],
					
	//we customize the XHTML structure of WYMeditor by overwriting 
	//the value of boxHtml. In this example, "CONTAINERS" and 
	//"CLASSES" have been moved from "wym_area_right" to "wym_area_top":
	boxHtml:   "<div class='wym_box'>"
		+ "<div class='wym_area_top'>"
		+ WYMeditor.TOOLS
		+ WYMeditor.CONTAINERS
		+ WYMeditor.CLASSES
		+ "</div>"
		+ "<div class='wym_area_left'></div>"
		+ "<div class='wym_area_right'>"
		+ "</div>"
		+ "<div class='wym_area_main'>"
		+ WYMeditor.HTML
		+ WYMeditor.IFRAME
		+ WYMeditor.STATUS
		+ "</div>"
		+ "<div class='wym_area_bottom'>"
		+ "</div>"
		+ "</div>",
	              
	postInit: function(wym) {
		jQuery(wym._box)
		    //first we have to select them:
		    .find(".wym_area_top .wym_panel")
		    //then we remove the existing class which make some of them render as a panels:
		    .removeClass("wym_panel")
		    //then we add the class which will make them render as a dropdown menu:
		    .addClass("wym_dropdown");
		
		jQuery(wym._box)
			.find(".wym_area_top .wym_dropdown")
		    //finally we add some css to make the dropdown menus look better:
		    .css("width", "160px")
		    .css("float", "left")
		    .css("margin-right", "5px")
		    .find("ul")
		    .css("width", "140px");
		    
		//add a ">" character to the title of the new dropdown menus (visual cue)
		jQuery(wym._box)
			.find(".wym_classes")
		    .find(WYMeditor.H2)
		    .append("<span>&nbsp;&gt;</span>");
	    
		wym.hovertools();
		wym.resizable();
	}
}