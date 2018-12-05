$(document).ready(function(){
    var stripe = Stripe('pk_test_OEiMPBtf9FhQ7ZM6rsjjFwKa');
    var elements = stripe.elements();
    var style = {
      base: {
        color: '#32325d',
        lineHeight: '18px',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
          color: '#aab7c4'
        }
      },
      invalid: {
        color: '#fa755a',
        iconColor: '#fa755a'
      }
    };
    // Create an instance of the card Element.
    var card = elements.create('card', {style: style});

    // Add an instance of the card Element into the `card-element` <div>.
    card.mount('#card-element');

    // Handle real-time validation errors from the card Element.
    card.addEventListener('change', function(event) {
      var displayError = document.getElementById('card-errors');
      if (event.error) {
        displayError.textContent = event.error.message;
      } else {
        displayError.textContent = '';
      }
    });

    var student_id = 0;
    var student_count = 0; //Initial field counter is 1
    var maxField = 4; //Input fields increment limitation
    var addButton = $('#add_button'); //Add button selector
    var wrapper = $('#student_wrapper'); //Input field wrapper
    var fieldHTML = '<div><input type="text" name="field_name[]" value=""/><a href="javascript:void(0);" class="remove_button"><img src="remove-icon.png"/></a></div>'; //New input field html 
    var bg_color = ['rgba(230, 181, 212, .7)', 'rgba(198, 135, 176, .8)', 'rgba(244, 243, 228, .5)', 'rgba(240, 222, 236, .5)'];
    var tuition_total = 0;

    $(addButton).click(function(){ 
        //Check maximum number of input fields
        student_id++;
        if(student_count < maxField){
            var new_student = '<div class="new_student" style="padding: 5px; margin: 5px; border-radius: 25px; float:left; overflow: hidden; background-color:' + bg_color.pop() + ';">' + 
                          '  <div class="form-row">' +
                          '     <div class="col-md-12">' +
                          '        <div class="col-md-6"><b>Student\'s Information</b></div>' +
                          '        <div class="col-md-6"><button style="float:right; color:#c687b0" class="remove_button"><span class="fas fa-trash-alt" class="remove_button"></span></button></div>' +
                          '     </div>' +
                          '  </div>' + 
                          '  <div class="form-row">' +
                          '    <div class="form-group col-md-6">' +
                          '      <label for="parent_first">Student\'s Full Name</label>' +
                          '      <input type="text" class="form-control" id="student_name" name="student_name_' + student_id + '"required>' +
                          '    </div>' +
                          '    <div class="form-group col-md-6">' +
                          '      <label for="parent_first">Student\'s Date of Birth</label>' +
                          '      <input type="text" class="form-control" id="student_birth_date"  name="student_birth_date_' + student_id + '" required>' +
                          '    </div>' +
                          '   </div>' +
                          '  <div class="form-row">' +
                          '    <div class="form-group col-md-12">' +
                          '      <label for="class_type">Select a Class</label>' +
                          '      <select class="form-control class_selection" id="class_id" name="student_class_id_' + student_id + '">' +
                          '        <option value="e4dd951e-0699-4dc1-92fc-de96ec37eb88">Pre-Ballet (ages 3-5): Mondays @ 10 - 10:45 AM ($30/month)</option>' +
                          '        <option value="24da8ed9-2866-46b9-a574-e6002fcb920a">Pre-Ballet (ages 3-5): Fridays @ 11:15 AM - 12 PM ($30/month)</option>' +
                          '        <option value="d3ddf124-d95b-4208-a4e9-627e14fb7c0a">Beginning Ballet (ages 6-10): Fridays @ 3:45 - 4:45 PM ($35/month)</option>' +
                          '        <option value="66825a33-86a9-425a-933c-951d24df0159">Adult Ballet (ages 18+): Wednesdays @ 8:15 - 9:30 PM ($40/month)</option>' +
                          '      </select>' +
                          '    </div>' +
                          '  </div>' +
                          '  <div class="form-row">' +
                          '    <div class="form-group col-md-12">' +
                          '      <label for=medical_id">Medical Concerns/Allergies</label>' +
                          '      <input type="text" class="form-control" id="medical_id" name="student_medical_id_' + student_id + '">' +
                          '    </div>' +
                          '  </div>' +
                          '</div>';

            student_count++; //Increment field counter
            $(wrapper).append(new_student); //Add field html
            recalculate();
        }
        else{
            alert("The maximum number of students you can register online is four. Please call 385-404-8687 to register.");
        }
    });

    //Let's start with at least one student   
    $(addButton).trigger("click");
 
    //Once remove button is clicked
    $(wrapper).on('click', '.remove_button', function(e){
        e.preventDefault();
        if (student_count == 1){
            alert("Must have at least one student.");
            return;
        }
        head_parent = $(this).parent('div').parent('div').parent('div').parent('div');
        bg_color.push(head_parent.css("background-color"));
        head_parent.remove(); //Remove field html
        student_count--; //Decrement field counter
        recalculate();
    });

    $(wrapper).on('change', '.class_selection', function(e){
        e.preventDefault();
        recalculate();
    });

    function recalculate(){
        var reg_fee = 0;
        if(student_count == 1){
            reg_fee = 10;
        }
        else if (student_count > 1){
            reg_fee = 15;
        }

        class_selections = get_classes();

        var class_uuids = [];
        for (i = 0; i < class_selections.length; i++){
            class_uuids.push(class_selections[i].value);
        }

        join_uuids = class_uuids.join();
        get_tuition_cost(join_uuids);
    }

    function get_tuition_cost(uuid_str){
        url = "https://localhost/tuition_total?class_selections=" + uuid_str
        $.ajax({
          type: "GET",
          url: url,
          success: function( cost ) {
            tuition_total = cost;
            set_cost_values();
          }
        });
    }

    function get_registration_fee(){
        if(student_count == 1){
            return 10;
        }
        else if (student_count > 1){
            return 15;
        }
        else{
            return 0;
        }
    }

    function get_classes(){
        return document.querySelectorAll(".class_selection");
    }

    function get_students(){
        return document.querySelectorAll(".new_student");
    }

    function set_cost_values(){
        registration_fee = get_registration_fee();
        if (registration_fee.valueOf() == String.prototype.toString()){
            total_cost = registration_fee;
        }
        else {
            total_cost = registration_fee + tuition_total;
        }
        document.getElementById('reg_fee').value = registration_fee;
        document.getElementById('tuition_fee').value = tuition_total;
        document.getElementById('total_cost').value = total_cost;
    }

    function is_verified(registration_data){
        url = "https://localhost/verify_reg_data"
        registration_data['csrfmiddlewaretoken'] = getCookie('csrftoken');
        $.ajax({
          type: "POST",
          url: url,
          data: registration_data,
          success: function( is_verified ) {
            if (is_verified) {
                submit_payment(registration_data);
            }
            else {
                alert("Problem verifying payment information. Please call 385-404-8687 to help process payment.");
            }
          }
        });
    }

    function getCookie(name) {
        var value = "; " + document.cookie;
        var parts = value.split("; " + name + "=");
        if (parts.length == 2) return parts.pop().split(";").shift();
    }

    function get_registration_form_data(){
        var registration_fee = document.getElementById('reg_fee').value;
        var tuition_fee = document.getElementById('tuition_fee').value;
        var total_fee = document.getElementById('total_cost').value;
        var student_elements = get_students();
        var student_list = []
        for(i=0; i<student_elements.length; i++){
            var student_ele = student_elements[i];
            var student_name = student_ele.querySelector("#student_name").value;
            var birth_date = student_ele.querySelector("#student_birth_date").value;
            var medical = student_ele.querySelector("#medical_id").value;
            var class_id = student_ele.querySelector(".class_selection").value;

            var student_info = { 'student_name': student_name,
                                 'birth_date': birth_date,
                                 'class_id': class_id,
                                 'medical': medical };

            student_list.push(student_info);
        }
        var reg_data = { 'reg_fee': registration_fee, 
                         'tuition_fee': tuition_fee,
                         'total_fee': total_fee,
                         'students': JSON.stringify(student_list) };

        return reg_data;
    }

    $('#registrationForm').on('submit', function(e, override=true){
        if (override) {
            e.preventDefault();
            if (student_count == 0){
                alert("Please add at least one student.");
                return;
            }
            registration_data = get_registration_form_data(); 
            verified = is_verified(registration_data);
        }
    });

    function submit_payment(data){
        total = parseInt(data['reg_fee'], 10) + parseInt(data['tuition_fee'], 10);
        
        stripe.createToken(card).then(function(result) {
          if (result.error) {
            var errorElement = document.getElementById('card-errors');
            errorElement.textContent = result.error.message;
          } else {
            // Send the token to your server.
            stripeTokenHandler(result.token);
            result = confirm("This will charge $" + total + " to your card. Press OK to complete registration.");
            if (result) {
                $('#registrationForm').trigger('submit', [false]);
            }
          }       
    });
  }
 
    // Submit the form with the token ID.
  function stripeTokenHandler(token) {
      // Insert the token ID into the form so it gets submitted to the server
      var form = document.getElementById('registrationForm');
      var hiddenInput = document.createElement('input');
      hiddenInput.setAttribute('type', 'hidden');
      hiddenInput.setAttribute('name', 'stripeToken');
      hiddenInput.setAttribute('value', token.id);
      form.appendChild(hiddenInput);

      // Let regstration.js perform the submission
      // form.submit();
  }
});

