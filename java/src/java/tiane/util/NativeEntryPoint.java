package tiane.util;

import java.lang.annotation.*;

/**
 * Markiert einen Einstiegspunkt für native Methoden. Dinge, die hiermit markiert sind, werden
 * von nativen Methoden entweder aufgerufen oder zugegriffen. Hauptnutzen sind IDEs, die Werte
 * dann nicht als ungenutzt anzeigen.
 */
@Documented
@Target({ElementType.METHOD, ElementType.FIELD, ElementType.CONSTRUCTOR})
@Retention(RetentionPolicy.CLASS)
public @interface NativeEntryPoint {
}
