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
    var bg_color = ['rgba(230, 181, 212, .7)', 'rgba(198, 135, 176, .8)', 'rgba(244, 243, 228, .5)', 'rgba(240, 222, 236, .5)'];
    var tuition_total = 0;

    var dance_classes = [];

    get_class_info();

    $(document).on('click', '#add_button', function(){
        dance_options = [];
        for(i=0; i<dance_classes.length; i++){
            next_class = dance_classes[i];

            if(next_class['has_room']){
              class_val = next_class['title'] + ' (ages ' + next_class['range'] + '): ' + next_class['day_of_week'] + ' @ ' + next_class['start_time'] + ' to ' + next_class['end_time'] + ' - ' + next_class['open_spots'] + ' spot(s) left';
              dance_options.push('<option value="' + next_class['id'] + '">' + class_val + '</option>');
            }
        }
        //Check maximum number of input fields
        if(student_count < maxField){
            student_id++;
            var new_student = '<div class="new_student" style="position:relative; z-index:10000; padding: 5px; margin: 5px; border-radius: 25px; float:left; background-color:' + bg_color.pop() + ';">' + 
                          '  <div class="form-row">' +
                          '     <div class="col-md-12">' +
                          '        <div class="col-md-12">' +
                          '          <b>Student\'s Information</b>' +
                          '          <span style="margin-top:5px; float: right; cursor: pointer;" class="fas fa-lg fa-trash-alt remove_button"></span>' + 
                          '        </div>' +
                          '     </div>' +
                          '  </div>' + 
                          '  <div class="form-row">' +
                          '    <div class="form-group col-md-6">' +
                          '      <label for="parent_first">Student\'s Full Name</label>' +
                          '      <input type="text" class="form-control student_name" name="student_name_' + student_id + '"required>' +
                          '    </div>' +
                          '    <div class="form-group col-md-6">' +
                          '      <label for="parent_first">Student\'s Date of Birth</label>' +
                          '      <input type="text" class="form-control student_birth_date"  name="student_birth_date_' + student_id + '" required>' +
                          '    </div>' +
                          '   </div>' +
                          '  <div class="form-row">' +
                          '    <div class="form-group col-md-12">' +
                          '      <label for="class_type">Select a Class</label>' +
                          '      <select class="form-control class_selection class_id" name="student_class_id_' + student_id + '">' +
                          dance_options.join() +
                          '      </select>' +
                          '    </div>' +
                          '  </div>' +
                          '  <div class="form-row">' +
                          '    <div class="form-group col-md-12">' +
                          '      <label for=medical_id">Medical Concerns/Allergies (Optional)</label>' +
                          '      <input type="text" class="form-control medical_id" name="student_medical_id_' + student_id + '">' +
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
 
    //Once remove button is clicked
    $(wrapper).on('click', 'span.remove_button', function(e){
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
            reg_fee = 15;
        }
        else if (student_count > 1){
            reg_fee = 25;
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
        url = "/tuition_total?class_selections=" + uuid_str
        $.ajax({
          type: "GET",
          url: url,
          success: function( cost ) {
            tuition_total = cost;
            set_cost_values();
          }
        });
    }

    function get_class_info(){
        url="/classes";
        $.ajax({
          type: "GET",
          url: url,
          success: function(data) {
              dance_classes = data;
              $(addButton).trigger("click");
          }
        });
    }

    function get_registration_fee(){
        if(student_count == 1){
            return 15;
        }
        else if (student_count > 1){
            return 20;
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
        url = "/verify_reg_data"
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
                alert("Please check that there is enough room in the class. If you continue to have problems, please call 385-404-8687.");
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
            var student_name = student_ele.querySelector(".student_name").value;
            var birth_date = student_ele.querySelector(".student_birth_date").value;
            var medical = student_ele.querySelector(".medical_id").value;
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

    $('#registrationForm').on('submit', function(e, override){
        if (override === undefined){
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
                $('#registrationForm').trigger('submit', [true]);
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

