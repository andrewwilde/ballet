<?php

require_once 'vendor/autoload.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\OAuth;
use PHPMailer\PHPMailer\Exception;
use League\OAuth2\Client\Provider\Google;

//require "vendor/phpmailer/phpmailer/src/PHPMailer.php";
//require "vendor/phpmailer/phpmailer/src/Exception.php";
//require "vendor/phpmailer/phpmailer/src/OAuth.php";

if(empty($_POST['name'])            ||
   empty($_POST['email'])           ||
   empty($_POST['message']) ||
   !filter_var($_POST['email'],FILTER_VALIDATE_EMAIL))
   {
    echo "No arguments Provided!";
    return false;
   }

$name = $_POST['name'];
$email_address = $_POST['email'];
$message = $_POST['message'];

// Create the email and send the message
$to = 'petitballetacademy@gmail.com'; // Add your email address inbetween the '' replacing yourname@yourdomain.com - This is where the form will send a message to.
$email_subject = "Website Contact Form:  $name";
$email_body = "You have received a new message from your website contact form.\n\n"."Here are the details:\n\nName: $name\n\nEmail: $email_address\n\nMessage:\n$message";
$headers = "From: noreply@ballet.com\n"; // This is the email address the generated message will be from. We recommend using something like noreply@yourdomain.com.
$headers .= "Reply-To: $email_address";

//$redirectUri = 'https://petitballetacademy.com/mail/get_oauth_token.php';
$clientId = '212720093318-sfhd9amqs4cpoiq0taggiiq81lc84tsr.apps.googleusercontent.com';
$clientSecret = '2qiRUnyfC7IK0Hh-Ryexomq6';
$refreshToken = '1/rJOVFa6XeOBIp2t2jAVL9iEqqlrPEnM6ze_vIoO5q-U';

$provider = new Google(
  [
    'clientId' => $clientId,
    'clientSecret' => $clientSecret
  ]
);

$mail = new PHPMailer();
$mail->isSMTP();
$mail->SMTPDebug = 4;
$mail->SMTPAuth = true;
$mail->SMTPSecure = 'tls';
$mail->Host = 'smtp.gmail.com';
$mail->Port = '587';
$mail->AuthType = 'XOAUTH2';

$mail->setOauth(
  new OAuth(
    [
      'provider' => $provider,
      'clientId' => $clientId,
      'clientSecret' => $clientSecret,
      'refreshToken' => $refreshToken,
      'userName' => $to
    ]
  )
);

$mail->isHTML();
$mail->Username = 'petitballetacademy@gmail.com';
$mail->Password = '*Ballet@22*';
$mail->setFrom('no-reply@petitballetacademy.com');
$mail->Subject = $email_subject;
$mail->Body = $email_body;
$mail->addAddress($to);

if(!$mail->send()) {
  echo "Mailer error: " . $mail->ErrorInfo;
} else {
  echo "Message Sent";
}

return true;
?>
