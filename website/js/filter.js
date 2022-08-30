var checkboxes = document.querySelectorAll(".categories input");
  for(var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].addEventListener("change", filter);
  }

  filter();
  function filter() {
    var i, j;
  
 
    // Get the selected categories
    var checkboxes = document.querySelectorAll(".categories input");
    var categories = [];
    var c;
    for(i = 0; i < checkboxes.length; i++) {
      if(checkboxes[i].checked) {
        c = checkboxes[i].value;
        categories.push(c);
      }
    }
  
    // Apply the filter
    var items = document.querySelectorAll(".filterDiv");
    var item, show;
    for(i = 0; i < items.length; i++) {
      item = items[i];
      if(categories.length == 0) {
        show = true;
      } else {
        // Intersection: All of the categories must apply
        show = true;
        for(j = 0; j < categories.length; j++) {
          if(!item.classList.contains(categories[j])) {
            show = false;
            break;
          }
        }
      }
  
      if(show) {
        item.classList.add("show");
      } else {
        item.classList.remove("show");
      }
    }
  }
