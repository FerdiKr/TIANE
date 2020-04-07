package tiane.java;

import tiane.java.api.LocalStorage;
import tiane.java.api.Module;
import tiane.java.api.ModuleContinuous;
import tiane.java.api.ModuleWrapper;

public class TIANEWrapper {

    public static native void startTiane(String runPy, String runDir, String[] dlopen);

    public static Module[] loadModules(String path) {
        //return ModuleFinder.findModules(path, Module.class).toArray(new Module[]{});

        return new Module[]{new Module() {

            @Override
            public String name() {
                return "javadummy";
            }

            @Override
            public int priority() {
                return 100;
            }

            @Override
            public String[] words() {
                return new String[]{"PINGUIN", "PANGOLIN"};
            }

            @Override
            public boolean isValid(String text) {
                text = text.toLowerCase();
                return text.contains("hallo") && text.contains("welt") && text.contains("pinguin");
            }

            @Override
            public boolean handle(String text, ModuleWrapper tiane, LocalStorage localStorage) {
                return false;
            }
        }};
    }

    public static ModuleContinuous[] loadModulesContinuous(String path) {
        return ModuleFinder.findModules(path, ModuleContinuous.class).toArray(new ModuleContinuous[]{});
    }
}
