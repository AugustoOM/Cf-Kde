// API comprobada con Plasma 6.7.5. Las pantallas se resuelven desde Plasma.
var existing = panels();
var managed = existing.filter(function(p) { p.currentConfigGroup=["CfKde"]; return p.readConfig("managed",false)===true || p.readConfig("managed","")==="true"; });
if(managed.length===0) existing.forEach(function(p){p.remove();});
function panelFor(screen, role) {
 var found = panels().filter(function(p){p.currentConfigGroup=["CfKde"];return p.screen===screen && p.readConfig("role","")===role;});
 if(found.length) return found[0];
 var p=new Panel("org.kde.panel");p.screen=screen;
 p.currentConfigGroup=["CfKde"];p.writeConfig("managed",true);p.writeConfig("role",role);
 return p;
}
function widget(p,type) {var w=p.widgets().filter(function(x){return x.type===type;});return w.length?w[0]:p.addWidget(type);}
function colorizer(p) {var c=widget(p,"luisbocanegra.panel.colorizer");c.currentConfigGroup=["General"];c.writeConfig("hideWidget",true);c.writeConfig("enableDBusService",true);c.reloadConfig();}
for(var s=0;s<screenCount;s++) {
 var top=panelFor(s,"top");top.location="top";top.height=38;top.lengthMode="fill";top.hiding="none";top.floating=false;top.opacity="translucent";
 var launcher=widget(top,"org.kde.plasma.kicker");launcher.currentConfigGroup=["General"];launcher.writeConfig("useCustomButtonImage",true);launcher.writeConfig("customButtonImage",__LAUNCHER_ICON__);launcher.reloadConfig();
 var menu=widget(top,"org.kde.plasma.appmenu");menu.currentConfigGroup=["General"];menu.writeConfig("compactView",false);menu.reloadConfig();
 var spacers=top.widgets().filter(function(w){return w.type==="org.kde.plasma.panelspacer";});
 while(spacers.length<2)spacers.push(top.addWidget("org.kde.plasma.panelspacer"));
 spacers.forEach(function(w){w.currentConfigGroup=["General"];w.writeConfig("expanding",true);w.reloadConfig();});
 var tray=widget(top,"org.kde.plasma.systemtray");
 var clock=widget(top,"org.kde.plasma.digitalclock");clock.currentConfigGroup=["Appearance"];
 clock.writeConfig("showSeconds",2);clock.writeConfig("showDate",true);clock.writeConfig("dateFormat","custom");clock.writeConfig("customDateFormat","dd/MM' -  'dddd dd 'de' MMMM' -'");clock.writeConfig("dateDisplayFormat",1);clock.writeConfig("use24hFormat",2);clock.writeConfig("autoFontAndSize",false);clock.writeConfig("fontFamily","Noto Sans");clock.writeConfig("fontSize",14);clock.writeConfig("fontWeight",700);clock.writeConfig("boldText",true);clock.writeConfig("fontStyleName","Bold");clock.reloadConfig();
 // Plasma 6's native spacers balance each side to keep the middle region centered.
 launcher.index=0;menu.index=1;spacers[0].index=2;clock.index=3;spacers[1].index=4;tray.index=5;
 colorizer(top);
 var dock=panelFor(s,"dock");dock.location="bottom";dock.height=64;dock.alignment="center";dock.lengthMode="fit";dock.hiding="autohide";dock.floating=true;dock.opacity="translucent";
 var tasks=widget(dock,"org.kde.plasma.icontasks");tasks.currentConfigGroup=["General"];
 tasks.writeConfig("launchers",__LAUNCHERS__);tasks.writeConfig("showOnlyCurrentScreen",true);tasks.writeConfig("fill",false);tasks.writeConfig("taskHoverEffect",false);tasks.writeConfig("showToolTips",true);tasks.writeConfig("maxStripes",1);tasks.reloadConfig();colorizer(dock);
 print("Cf-Kde: screen="+s+" geometry="+JSON.stringify(screenGeometry(s))+" top="+top.id+" dock="+dock.id);
}
