import org.jetbrains.kotlin.gradle.tasks.KotlinCompile
import kr.entree.spigradle.kotlin.*

plugins {
    kotlin("jvm") version "1.7.10"
    id("xyz.jpenilla.run-paper") version "1.0.6"
    id("kr.entree.spigradle") version "2.4.2"
}

group = "com.jackharrhy.cheesedata"
version = "1.0-SNAPSHOT"

dependencies {
    implementation(kotlin("stdlib-jdk8"))
    compileOnly(spigot("1.19.2"))
}

spigot {
    commands {
        create("cheesedata") {
            aliases = listOf("cd")
        }
    }
}

tasks.withType<KotlinCompile> {
    kotlinOptions.jvmTarget = "1.8"
}

tasks.runServer {
    minecraftVersion("1.19.2")
}