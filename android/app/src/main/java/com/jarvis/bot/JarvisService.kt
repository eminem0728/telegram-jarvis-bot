package com.jarvis.bot

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.net.wifi.WifiManager
import android.os.Build
import android.os.IBinder
import android.os.PowerManager
import android.util.Log
import com.chaquo.python.Python

class JarvisService : Service() {

    private var botThread: Thread? = null
    private var wakeLock: PowerManager.WakeLock? = null
    private var wifiLock: WifiManager.WifiLock? = null

    override fun onCreate() {
        super.onCreate()
        startForeground(1, buildNotification("Jarvis запускается..."))
        val pm = getSystemService(Context.POWER_SERVICE) as PowerManager
        wakeLock = pm.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK, "JarvisBot::lock").apply { acquire() }
        val wm = applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
        wifiLock = wm.createWifiLock(WifiManager.WIFI_MODE_FULL_HIGH_PERF, "JarvisBot::wifi").apply { acquire() }
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        if (botThread?.isAlive == true) return START_STICKY
        val prefs = getSharedPreferences("jarvis", Context.MODE_PRIVATE)
        val token = prefs.getString("token", "") ?: ""
        val zen = prefs.getString("zen", "") ?: ""
        if (token.isBlank()) {
            updateNotification("Нет TELEGRAM_TOKEN — открой приложение")
            return START_STICKY
        }
        botThread = Thread({
            try {
                updateNotification("Jarvis работает")
                if (!Python.isStarted()) Python.start(com.chaquo.python.android.AndroidPlatform(this))
                val py = Python.getInstance()
                // filesDir нужен python-коду для json/истории
                py.getModule("bot_main").callAttr("start_bot", filesDir.absolutePath, token, zen)
            } catch (e: Exception) {
                Log.e("Jarvis", "bot crash", e)
                updateNotification("Упал, перезапуск через 5с: ${e.message}")
                try { Thread.sleep(5000) } catch (_: Exception) {}
                // перезапуск
                if (prefs.getBoolean("enabled", true)) onStartCommand(null, flags, startId)
            }
        }, "jarvis-bot").apply { start() }
        return START_STICKY
    }

    override fun onDestroy() {
        try {
            // Python-поток прервется вместе с сервисом; при enabled=true BootReceiver/Service перезапустит
            botThread?.interrupt()
            wakeLock?.let { if (it.isHeld) it.release() }
            wifiLock?.let { if (it.isHeld) it.release() }
        } catch (_: Exception) {}
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null

    private fun buildNotification(text: String): Notification {
        val chId = "jarvis"
        val nm = getSystemService(NotificationManager::class.java)
        if (Build.VERSION.SDK_INT >= 26) {
            nm.createNotificationChannel(NotificationChannel(chId, "Jarvis", NotificationManager.IMPORTANCE_LOW))
        }
        val pi = PendingIntent.getActivity(this, 0, Intent(this, MainActivity::class.java),
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT)
        return if (Build.VERSION.SDK_INT >= 26) {
            Notification.Builder(this, chId)
                .setContentTitle("Jarvis Bot")
                .setContentText(text)
                .setSmallIcon(android.R.drawable.ic_dialog_info)
                .setContentIntent(pi)
                .setOngoing(true)
                .build()
        } else {
            @Suppress("DEPRECATION")
            Notification.Builder(this)
                .setContentTitle("Jarvis Bot")
                .setContentText(text)
                .setSmallIcon(android.R.drawable.ic_dialog_info)
                .setContentIntent(pi)
                .setOngoing(true)
                .build()
        }
    }

    private fun updateNotification(text: String) {
        (getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager).notify(1, buildNotification(text))
    }
}
