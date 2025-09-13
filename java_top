package com.example.binofor;

import android.app.AlarmManager;
import android.app.DatePickerDialog;
import android.app.PendingIntent;
import android.app.TimePickerDialog;
import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.util.Log;
import android.widget.Button;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.google.android.material.textfield.TextInputEditText;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.messaging.FirebaseMessaging;

import java.util.Calendar;
import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivity";
    private TextInputEditText nameInput;
    private TextInputEditText phoneInput;
    private TextInputEditText commentInput;
    private Button dateButton;
    private Button timeButton;
    private Button submitButton;
    private Button viewAppointmentsButton;

    private Calendar selectedDateTime;
    private FirebaseFirestore db;
    private String fcmToken;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Initialize Firestore
        db = FirebaseFirestore.getInstance();
        selectedDateTime = Calendar.getInstance();

        // Get FCM token
        getFCMToken();

        // Initialize views
        nameInput = findViewById(R.id.nameInput);
        phoneInput = findViewById(R.id.phoneInput);
        commentInput = findViewById(R.id.commentInput);
        dateButton = findViewById(R.id.dateButton);
        timeButton = findViewById(R.id.timeButton);
        submitButton = findViewById(R.id.submitButton);
        viewAppointmentsButton = findViewById(R.id.viewAppointmentsButton);

        // Set up date picker
        dateButton.setOnClickListener(v -> showDatePicker());

        // Set up time picker
        timeButton.setOnClickListener(v -> showTimePicker());

        // Set up submit button
        submitButton.setOnClickListener(v -> submitAppointment());

        // Set up view appointments button
        viewAppointmentsButton.setOnClickListener(v -> {
            Intent intent = new Intent(MainActivity.this, AppointmentsActivity.class);
            startActivity(intent);
        });
    }

    private void getFCMToken() {
        FirebaseMessaging.getInstance().getToken()
            .addOnCompleteListener(task -> {
                if (!task.isSuccessful()) {
                    Log.w(TAG, "Fetching FCM registration token failed", task.getException());
                    return;
                }

                // Get new FCM registration token
                fcmToken = task.getResult();
                Log.d(TAG, "FCM Token: " + fcmToken);
            });
    }

    private void showDatePicker() {
        DatePickerDialog datePickerDialog = new DatePickerDialog(
            this,
            (view, year, month, dayOfMonth) -> {
                selectedDateTime.set(Calendar.YEAR, year);
                selectedDateTime.set(Calendar.MONTH, month);
                selectedDateTime.set(Calendar.DAY_OF_MONTH, dayOfMonth);
                updateDateButtonText();
            },
            selectedDateTime.get(Calendar.YEAR),
            selectedDateTime.get(Calendar.MONTH),
            selectedDateTime.get(Calendar.DAY_OF_MONTH)
        );
        datePickerDialog.show();
    }

    private void showTimePicker() {
        TimePickerDialog timePickerDialog = new TimePickerDialog(
            this,
            (view, hourOfDay, minute) -> {
                selectedDateTime.set(Calendar.HOUR_OF_DAY, hourOfDay);
                selectedDateTime.set(Calendar.MINUTE, minute);
                updateTimeButtonText();
            },
            selectedDateTime.get(Calendar.HOUR_OF_DAY),
            selectedDateTime.get(Calendar.MINUTE),
            true
        );
        timePickerDialog.show();
    }

    private void updateDateButtonText() {
        String date = String.format("%02d.%02d.%d",
            selectedDateTime.get(Calendar.DAY_OF_MONTH),
            selectedDateTime.get(Calendar.MONTH) + 1,
            selectedDateTime.get(Calendar.YEAR));
        dateButton.setText(date);
    }

    private void updateTimeButtonText() {
        String time = String.format("%02d:%02d",
            selectedDateTime.get(Calendar.HOUR_OF_DAY),
            selectedDateTime.get(Calendar.MINUTE));
        timeButton.setText(time);
    }

    private void submitAppointment() {
        String name = nameInput.getText().toString().trim();
        String phone = phoneInput.getText().toString().trim();
        String comment = commentInput.getText().toString().trim();

        if (TextUtils.isEmpty(name) || TextUtils.isEmpty(phone)) {
            Toast.makeText(this, "Заполните обязательные поля", Toast.LENGTH_SHORT).show();
            return;
        }

        String date = String.format("%02d.%02d.%d",
            selectedDateTime.get(Calendar.DAY_OF_MONTH),
            selectedDateTime.get(Calendar.MONTH) + 1,
            selectedDateTime.get(Calendar.YEAR));
        
        String time = String.format("%02d:%02d",
            selectedDateTime.get(Calendar.HOUR_OF_DAY),
            selectedDateTime.get(Calendar.MINUTE));

        Map<String, Object> appointment = new HashMap<>();
        appointment.put("name", name);
        appointment.put("phone", phone);
        appointment.put("date", date);
        appointment.put("time", time);
        appointment.put("comment", comment);
        appointment.put("timestamp", Calendar.getInstance().getTimeInMillis());
        appointment.put("fcmToken", fcmToken);

        db.collection("appointments")
            .add(appointment)
            .addOnSuccessListener(documentReference -> {
                Toast.makeText(MainActivity.this, "Запись успешно создана", Toast.LENGTH_SHORT).show();
                clearForm();
            })
            .addOnFailureListener(e -> {
                Toast.makeText(MainActivity.this, "Ошибка при создании записи: " + e.getMessage(), 
                    Toast.LENGTH_SHORT).show();
            });
    }

    private void clearForm() {
        nameInput.setText("");
        phoneInput.setText("");
        commentInput.setText("");
        selectedDateTime = Calendar.getInstance();
        dateButton.setText("Выбрать дату");
        timeButton.setText("Выбрать время");
    }
} 
