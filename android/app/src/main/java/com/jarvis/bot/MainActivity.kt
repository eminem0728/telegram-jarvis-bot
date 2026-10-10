package com.jarvis.bot

import android.content.Context
import android.content.Intent
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.os.PowerManager
import android.provider.Settings
import android.widget.Button
import android.widget.EditText
import android.widget.ScrollView
import android.widget.TextView
import android.widget.LinearLayout
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat

class MainActivity : AppCompatActivity() {

    private lateinit var prefs: android.content.SharedPreferences
    private lateinit var logView: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        prefs = getSharedPreferences("jarvis", Context.MODE_PRIVATE)

        val layout = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(32, 32, 32, 32)
        }

        val tokenField = EditText(this).apply {
            hint = "TELEGRAM_TOKEN"
            setText(prefs.getString("token", ""))
        }
        val zenField = EditText(this).apply {
            hint = "OPENCODE_ZEN_API_KEY"
            setText(prefs.getString("zen", ""))
        }
        val btnOn = Button(this).apply { text = "▶ ВКЛЮЧИТЬ БОТА" }
        val btnOff = Button(this).apply { text = "■ ВЫКЛЮЧИТЬ" }
        val btnBattery = Button(this).apply { text = "Убрать оптимизацию батареи" }
        logView = TextView(this).apply { text = "Лог появится здесь.\n" }
        val scroll = ScrollView(this).apply { addView(logView) }

        layout.addView(tokenField)
        layout.addView(zenField)
        layout.addView(btnOn)
        layout.addView(btnOff)
        layout.addView(btnBattery)
        layout.addView(scroll)
        setContentView(layout)

        if (Build.VERSION.SDK_INT >= 33) {
            ActivityCompat.requestPermissions(this, arrayOf(android.Manifest.permission.POST_NOTIFICATIONS), 1)
        }

        btnOn.setOnClickListener {
            prefs.edit()
                .putString("token", tokenField.text.toString().trim())
                .putString("zen", zenField.text.toString().trim())
                .putBoolean("enabled", true)
                .apply()
            val i = Intent(this, JarvisService::class.java)
            if (Build.VERSION.SDK_INT >= 26) startForegroundService(i) else startService(i)
            log("Запуск...")
        }
        btnOff.setOnClickListener {
            prefs.edit().putBoolean("enabled", false).apply()
            stopService(Intent(this, JarvisService::class.java))
            log("Остановлен.")
        }
        btnBattery.setOnClickListener {
            try {
                val pm = getSystemService(Context.POWER_SERVICE) as PowerManager
                if (!pm.isIgnoringBatteryOptimizations(packageName)) {
                    startActivity(Intent(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS, Uri.parse("package:$packageName")))
                } else {
                    log("Оптимизация уже отключена.")
                }
            } catch (e: Exception) {
                log("Ошибка: ${e.message}")
            }
        }
    }

    private fun log(s: String) {
        runOnUiThread { logView.append(s + "\n") }
    }
}
