import os
import shutil
from git import Repo
import git
from pathlib import Path
import random
import string

LINE = 32
N_LINES = 50
TOKEN = "my-ctf-token"
REMOTE = "my-remote"
PEOPLE_MAIN = 15
PEOPLE_END = 23

TEXT = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque nec mi mollis, finibus dolor eu, mollis magna. Mauris ac tellus urna. Fusce volutpat euismod ex non gravida. Quisque ante quam, ultrices eget posuere molestie, mollis pulvinar nunc. Aenean rhoncus, nunc sit amet euismod iaculis, lectus nisi semper dui, non lacinia velit risus at elit. Maecenas augue urna, tempor eu nunc et, tincidunt porttitor magna. Sed ullamcorper neque at urna malesuada, ut ornare sapien hendrerit. In sed vehicula neque. Etiam a aliquet nibh. Nulla quis nulla felis. Sed quis volutpat neque. Duis id venenatis libero, vitae ullamcorper diam. Morbi id elementum urna, quis aliquam erat. Vivamus sollicitudin, nunc eu blandit tempor, tellus ligula tristique diam, nec fringilla metus purus et diam. Donec feugiat libero sed libero suscipit luctus. Aenean sit amet placerat nulla, a aliquam massa.
Nunc vestibulum nulla odio, sit amet dignissim libero pretium a. Donec id finibus arcu, a condimentum urna. Donec at elit id massa vulputate sagittis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Vivamus lacinia a mi eu aliquam. Aliquam eleifend nisi quis vulputate ullamcorper. Nullam ornare id purus eu scelerisque. Maecenas egestas iaculis dui, sed euismod velit auctor sed. Donec lorem massa, hendrerit ac varius non, viverra id nunc. Nulla luctus, elit sit amet egestas ornare, ipsum lacus elementum sem, in consequat risus enim sed justo. In finibus venenatis libero, eu interdum diam cursus non. Suspendisse tincidunt porta turpis, egestas ullamcorper nulla viverra at. Integer non neque tellus. Aliquam lobortis, magna sed auctor volutpat, ante sapien scelerisque dolor, non interdum magna metus vitae metus. Aliquam vitae felis rhoncus, lobortis orci et, porta risus. Praesent et lectus ornare, condimentum turpis commodo, feugiat nibh.
Integer varius non orci scelerisque feugiat. Donec consectetur neque in mauris ornare imperdiet. Nullam consectetur, dui id convallis pretium, eros magna interdum ipsum, sed efficitur leo arcu et velit. Praesent auctor sit amet tellus ac pulvinar. Suspendisse sodales nisi sed odio tempus laoreet. Pellentesque nec libero turpis. Phasellus imperdiet elit ac elementum eleifend.
Ut mollis ligula sed mauris posuere cursus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sodales in metus et cursus. Cras interdum aliquet elit non gravida. Donec vitae nisi nisl. Nulla eu eros ac turpis feugiat aliquam nec quis augue. Ut dapibus orci et lacinia blandit. Cras porta feugiat velit, vitae sodales magna tempus vitae. Phasellus eget odio in nibh sodales tempor sit amet porttitor ligula. Morbi sodales quis eros nec mollis. Proin non tellus sit amet ex efficitur consectetur.
Duis tempor fringilla nisl et lacinia. In facilisis ex at orci consectetur eleifend. Curabitur bibendum felis sed velit venenatis bibendum. Donec dignissim turpis nec tortor tincidunt, in fermentum ligula suscipit. Curabitur rutrum fermentum odio, sit amet egestas sapien vehicula at. Sed id leo ultrices, bibendum risus ut, facilisis lorem. Cras in gravida neque. Fusce in lacus sed felis feugiat faucibus. Pellentesque a dolor vehicula, egestas mauris at, fermentum magna. Ut id ornare eros. Integer ligula lacus, aliquam eu tincidunt sit amet, faucibus in est. Maecenas gravida tortor lectus, a rhoncus libero blandit ut. Mauris aliquam euismod metus et molestie. Nullam mollis odio mauris, at tempus libero mattis eget. Mauris dui arcu, posuere a dignissim et, aliquet condimentum neque. Duis nibh metus, cursus vel laoreet at, sodales in lacus.
Sed molestie, augue ut consectetur convallis, neque nibh semper lacus, at fringilla massa est vitae nibh. Integer non pulvinar arcu, vel pharetra orci. Morbi feugiat dui et ullamcorper dignissim. Proin sed hendrerit tellus, tempor lobortis nisi. Morbi at tincidunt eros. Etiam at ultricies arcu. Pellentesque convallis dolor ac massa fringilla feugiat. Etiam a dui justo. Sed vitae tortor velit. Morbi laoreet nulla dolor, sit amet pulvinar magna accumsan in. Proin diam tortor, viverra in commodo id, fermentum id ipsum. Cras nec ex non elit tincidunt sodales at eu mi. Integer quam diam, pulvinar sit amet augue eget, interdum pretium ante. Suspendisse potenti. Nullam pharetra leo sit amet mauris tincidunt, nec vestibulum orci volutpat.
In euismod libero quis quam posuere vehicula. Donec ullamcorper pulvinar tincidunt. Duis id velit vitae tortor scelerisque malesuada non vitae nisi. Phasellus vitae tortor vitae enim aliquet mollis. Proin lacinia nisi quis rhoncus auctor. Praesent maximus scelerisque nunc, ut feugiat massa tincidunt eu. Fusce eget tincidunt dolor, id tincidunt libero. Nam fermentum, nisl at ullamcorper laoreet, arcu neque porta ex, id blandit velit urna in nunc. Nulla pulvinar lacinia enim, nec sodales nisi semper interdum. Aliquam mattis lacus sit amet eros sollicitudin scelerisque. Nullam at tristique dolor. Donec sollicitudin posuere dolor eu congue. Vivamus dignissim tortor ac tortor elementum consectetur. Donec porta dui in velit blandit aliquam.
In posuere tortor urna, eu cursus justo pretium a. Donec faucibus porttitor varius. Nunc vitae commodo nunc. Fusce interdum accumsan nisl at congue. Proin eu lacus semper, suscipit justo sed, tristique lacus. Maecenas nec erat at augue faucibus ornare. Proin magna orci, vestibulum vitae mi eget, efficitur congue velit. Phasellus ligula lorem, fermentum eu viverra ut, cursus sit amet felis. Curabitur et leo nibh. Integer a aliquet magna. Duis fermentum dui at nibh tincidunt, a fermentum nunc tempus. Etiam ut scelerisque mi. Integer pellentesque ut felis ac pretium. Donec turpis neque, malesuada eu ipsum quis, consequat rutrum turpis. Sed vitae bibendum velit. Nunc cursus condimentum consequat.
Vivamus lobortis ultricies ex, eget lobortis lacus cursus suscipit. Nunc commodo rutrum venenatis. Nullam suscipit mattis urna, eget euismod lorem fermentum nec. Nulla facilisi. Quisque volutpat orci sed velit tincidunt auctor. Cras rutrum dignissim dolor, ac vehicula turpis. Duis nisi nisl, ultricies quis arcu vel, efficitur posuere mauris. Fusce ut augue est. Phasellus euismod, magna id maximus cursus, magna massa egestas ante, et consequat leo risus ut ex. Aliquam id leo eu mi pretium viverra eget a dui. Sed ornare orci nibh, sit amet pulvinar sem auctor ut. Sed risus tortor, rutrum a pharetra ut, lobortis non urna. Maecenas quis bibendum metus. Nam at risus lectus. Suspendisse lobortis, elit ac scelerisque porttitor, lorem lectus aliquam ex, ut scelerisque dui enim quis nisl. Nulla ultrices nisl ligula, sit amet suscipit eros iaculis ac.
Fusce rhoncus feugiat enim. In efficitur risus sapien, a maximus purus fermentum et. Sed porta dignissim libero, et fermentum elit feugiat at. Vestibulum eu tellus sit amet nulla hendrerit dignissim eget nec dui. Etiam posuere id magna congue aliquet. Vivamus maximus sagittis ipsum ut varius. In ut ipsum eget leo blandit tempus et vitae magna.
Integer iaculis, justo sed mollis ornare, diam ipsum tristique nulla, non aliquet odio orci quis velit. In ut bibendum ante, vitae convallis purus. Donec finibus elementum arcu, in blandit justo ornare eget. Ut blandit ipsum orci, quis porttitor nisl finibus sit amet. Etiam risus ligula, posuere eu mauris non, rhoncus imperdiet sapien. Nunc volutpat orci felis, non sodales ante elementum quis. Nunc orci ante, commodo nec feugiat et, consequat at nunc. Aenean placerat erat at risus vehicula, vel rhoncus justo varius. In pharetra nunc ac nisl imperdiet dictum. Nunc in purus sapien. Fusce molestie id arcu dictum dictum.
Aliquam varius blandit dapibus. Aenean sit amet dolor a lorem consectetur porta vel quis libero. Morbi molestie mi et arcu sollicitudin, id varius erat tincidunt. Maecenas in ultrices lectus, ut ullamcorper mauris. Mauris id erat eget nunc tempus porta. Pellentesque et semper ante, vulputate auctor erat. Quisque elementum nec tortor ut molestie. Quisque mollis, quam quis semper tristique, mi sapien rutrum lorem, a mollis tortor massa a massa. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aenean fringilla erat arcu, a finibus est pretium ac. Proin augue sem, cursus et scelerisque non, dapibus ut dui. Aliquam quam libero, tristique et dignissim non, pellentesque id ex. Nunc feugiat lorem at enim rutrum sollicitudin. Vivamus vel luctus metus.
Curabitur ipsum neque, ultrices at rutrum in, tincidunt in orci. Ut sit amet arcu justo. Etiam dictum tortor arcu, et pellentesque velit condimentum quis. Nulla facilisis ante eget diam interdum ornare. Ut nisi quam, accumsan quis ultrices vel, luctus non quam. Sed consectetur mattis dictum. Aliquam placerat quis augue vitae accumsan. Fusce nisi ex, placerat a augue eu, ultricies rutrum erat. Proin sed nisl nunc. Sed egestas efficitur urna at cursus.
Donec tellus tortor, molestie id est sed, mattis egestas est. In in commodo nisl. Aenean varius ante at arcu venenatis faucibus. Aliquam ipsum ex, tristique non tortor eu, accumsan vehicula orci. Praesent semper sed sem nec aliquet. Curabitur efficitur, nisi vitae scelerisque suscipit, ex felis tempus leo, vel tempus sapien dolor ut urna. Pellentesque convallis tincidunt ex, vel finibus elit fringilla ut. Quisque et ligula sollicitudin, ullamcorper risus non, scelerisque mauris. Donec suscipit nec massa non dictum. Suspendisse velit tellus, viverra eget ipsum a, lacinia aliquam elit.
Etiam vehicula libero id tortor placerat, ac tristique ligula congue. Fusce aliquam volutpat lectus, quis varius nunc ullamcorper in. In felis lectus, pulvinar sit amet lobortis non, elementum sit amet ipsum. Nullam ornare aliquam finibus. Morbi vulputate pharetra ante, ac gravida nisi porta quis. Pellentesque cursus purus ut dictum porta. Suspendisse malesuada dignissim ligula. Integer volutpat sit amet diam quis tempus. Proin sit amet pretium ante, id pulvinar tortor. Etiam in posuere quam, vel vestibulum metus. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Pellentesque et felis enim. Duis eu vehicula eros. Integer et diam nulla. Quisque porta tortor id nisi eleifend, ut mattis est lobortis. Sed posuere purus et arcu lacinia, nec efficitur nunc volutpat.
Aenean ornare felis non dictum accumsan. Integer vel nisl vitae elit fringilla tristique. Donec interdum fermentum nibh nec accumsan. Sed eget efficitur lorem. Vestibulum efficitur accumsan ex, eu ultricies arcu volutpat a. Sed pulvinar augue in ligula rhoncus, vitae rhoncus lacus tempus. Nulla placerat finibus felis vel egestas.
Aliquam non dolor congue, euismod ligula eu, egestas ex. Sed egestas consectetur sagittis. Donec ac turpis magna. Aliquam erat volutpat. Quisque a iaculis libero, in auctor tellus. Morbi mauris libero, rhoncus vitae dignissim vel, fringilla gravida velit. Integer eget volutpat felis. Phasellus dictum velit sed semper feugiat. Vivamus nec maximus ex, nec vestibulum arcu. Ut venenatis vehicula justo, et mollis velit placerat a. Suspendisse dapibus mauris vel ex hendrerit pellentesque.
Sed sagittis neque ac consectetur cursus. Quisque nisl dui, finibus auctor justo non, tempus porta lectus. Proin consequat, nulla sit amet viverra semper, est diam vehicula velit, sed scelerisque turpis elit in tellus. Integer fermentum, enim gravida elementum varius, ante ante tincidunt nibh, dictum laoreet sapien risus sed lorem. Cras leo odio, tristique vel venenatis et, euismod vitae mauris. Sed tincidunt dolor sit amet dui sodales sagittis. Cras eget ipsum lorem. Integer viverra mi ut sagittis euismod. Curabitur turpis mauris, mattis ut posuere congue, iaculis ac augue. Cras sollicitudin pellentesque fermentum. Proin laoreet, ante ac hendrerit fermentum, ante lectus pellentesque lectus, eget dapibus ante lectus et est.
Praesent dignissim vestibulum ante, volutpat elementum dui vehicula a. Maecenas ipsum lectus, cursus nec rhoncus eget, dictum non orci. Donec lacinia dapibus elit vel finibus. Nullam condimentum pharetra lorem, quis accumsan nulla elementum ut. Maecenas efficitur magna sit amet mauris tempor mollis. Nullam molestie vulputate odio, eu tristique diam viverra at. Maecenas faucibus feugiat enim a ullamcorper. Sed tristique luctus tortor id congue. Proin vitae dapibus nisl. Quisque eget tincidunt nunc. Quisque vestibulum et tellus a congue. Ut elit odio, malesuada tempor orci vel, fringilla varius mi. Maecenas at libero in leo fermentum placerat.
Ut aliquam blandit tristique. Sed ac pharetra mauris. Duis nec neque vitae nibh tincidunt vestibulum. Duis tellus felis, lobortis vitae nulla et, tincidunt pellentesque leo. Donec euismod ipsum id erat vestibulum, ut eleifend lectus convallis. Etiam in tincidunt nunc. Morbi ut posuere neque. Duis tempus, lorem a fringilla aliquam, elit quam dapibus lorem, et mattis nunc orci suscipit tellus. Quisque efficitur laoreet ipsum quis venenatis. Integer sagittis nunc ac eros varius tempor. Aliquam lorem eros, tristique sed nisi eget, fringilla semper dui. Sed lorem ante, vestibulum vitae justo interdum, auctor aliquet mi. Phasellus nibh justo, elementum nec pulvinar nec, ultricies a mi. Nulla arcu ipsum, lacinia nec velit lacinia, facilisis sodales sem.
Vivamus auctor dignissim nunc eu pretium. Maecenas vitae blandit metus. Pellentesque vitae dolor ex. Curabitur et mollis libero. Sed venenatis massa eros, vel ultricies odio rhoncus non. Nunc quis pellentesque nunc. Nulla efficitur nec ligula id ultricies. Suspendisse ac elit euismod, pulvinar nulla ut, rhoncus arcu. Donec a suscipit neque, quis vehicula mi. Fusce rhoncus posuere ante, quis vehicula est bibendum quis. Proin porttitor commodo augue, in placerat odio facilisis in. Integer scelerisque blandit tortor nec mollis. Fusce a sagittis nibh, nec faucibus augue. Proin eu maximus tortor. Proin id elementum purus, eget vestibulum ante. Donec faucibus luctus eros a viverra.
Suspendisse vestibulum, turpis a gravida consequat, quam nulla commodo ante, et consequat nisi ante a diam. Etiam hendrerit suscipit interdum. Praesent sagittis venenatis commodo. Sed vestibulum vitae lectus eu vehicula. Mauris sem leo, cursus quis diam sed, molestie convallis elit. Maecenas faucibus pulvinar massa, eu aliquam erat iaculis non. Nunc vel nisi ac nibh pharetra pretium eget pulvinar orci.
Curabitur dignissim tristique aliquet. Suspendisse suscipit, nisl non finibus hendrerit, enim ipsum malesuada ipsum, et dignissim enim eros id lorem. Nulla convallis suscipit felis in consequat. Curabitur id felis elementum, molestie dui at, ullamcorper sem. Sed tempor volutpat lorem, vel feugiat leo faucibus sed. Sed lorem nibh, commodo quis massa vitae, luctus vehicula lacus. Donec ac semper eros. Curabitur finibus a augue a congue. Donec mauris mi, rhoncus a lacinia sed, molestie vitae diam. Phasellus eget est turpis. Vestibulum at lectus ipsum. Nulla commodo risus magna, vulputate lobortis est eleifend vel. Proin vel diam in sem vehicula sagittis. Nulla arcu dui, sollicitudin quis suscipit at, vestibulum et orci. Fusce iaculis ex sit amet venenatis auctor.
Pellentesque cursus turpis in purus finibus rhoncus. Donec placerat sapien quis viverra iaculis. Etiam in ligula nisi. Nullam ornare consectetur tortor et scelerisque. Nullam et orci a sem dapibus tristique. Sed mattis, dolor a convallis feugiat, massa purus hendrerit mi, sit amet tempus sapien libero vel metus. Praesent diam felis, tincidunt in lorem at, ultricies lobortis augue. Fusce id blandit ex, in consectetur elit.
Proin porttitor pellentesque leo quis efficitur. Curabitur condimentum venenatis congue. Mauris dignissim nisi nec diam suscipit, quis pretium tellus mattis. Curabitur condimentum lectus ut metus tempus pretium. Donec nec imperdiet quam. Nullam non vulputate tellus, at finibus arcu. Nam dolor neque, fringilla eget ornare et, venenatis eu sem. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aliquam sit amet nunc orci.
Nunc bibendum risus purus, sit amet rhoncus risus rutrum ac. Sed feugiat est at neque feugiat, ut hendrerit quam posuere. Donec aliquet, velit sed viverra sollicitudin, elit lectus suscipit lectus, non rutrum purus magna nec nisl. Etiam eget nisl eu justo mollis placerat sit amet congue enim. Vivamus tortor ex, commodo ut vestibulum sed, tristique eu diam. Phasellus volutpat lobortis nunc. Duis auctor lacus nec est porta pellentesque. Quisque sed pellentesque lectus. Sed vel orci magna. Proin elementum ipsum quis massa vestibulum, sed vehicula neque pretium.
Proin est est, pharetra et imperdiet sit amet, facilisis sed erat. Proin egestas erat nec nibh convallis, nec commodo nunc pretium. Donec arcu libero, aliquam nec felis ac, commodo aliquet felis. Morbi suscipit nisi eget ultrices ultricies. Vivamus luctus dignissim orci, in fermentum elit accumsan in. Aenean efficitur diam a enim fringilla laoreet. Donec cursus euismod pellentesque. Maecenas ut nisi interdum, feugiat orci sed, vulputate orci. Aliquam aliquet libero eu massa eleifend, ac tincidunt erat pharetra. Nulla facilisi. Ut vel pellentesque metus. Phasellus at placerat ligula. Aliquam luctus est eget vulputate fermentum. Morbi pellentesque tellus justo, id aliquet arcu rhoncus et. Vivamus quis iaculis metus.
Etiam mauris urna, sagittis sed commodo ut, elementum vel velit. Morbi arcu nunc, elementum vel bibendum eget, accumsan ut enim. Sed eu accumsan velit, et ullamcorper urna. Vivamus scelerisque iaculis enim vitae condimentum. Sed sit amet mauris sed erat pharetra rutrum. Quisque erat metus, posuere sed vulputate eget, accumsan in justo. Pellentesque vitae enim sed lectus facilisis pretium a eget arcu. Fusce mattis eu elit ut malesuada. Ut malesuada faucibus ex nec congue. Integer elementum auctor maximus.
Proin faucibus turpis eget urna placerat vehicula. Nunc mollis tempor urna non placerat. Nullam aliquet neque vel leo luctus, vitae porta nulla ornare. Quisque ullamcorper ultrices nisi, nec accumsan ligula posuere eget. Suspendisse potenti. Nulla est urna, venenatis non nunc ac, ullamcorper pulvinar purus. Vivamus sed nunc non tortor condimentum facilisis. Quisque egestas convallis euismod. Maecenas non nunc ultricies, semper leo ac, sagittis nisi. Nunc gravida ultricies mauris ullamcorper tincidunt. Ut quis sem fringilla, luctus leo at, aliquam velit. Nulla a semper orci. Phasellus et metus nunc. Etiam gravida arcu ut orci hendrerit vehicula. Nam diam nisi, efficitur vel est nec, placerat eleifend dui. Aliquam ac ex libero.
Vestibulum et euismod leo. Nullam feugiat turpis id ex commodo, vel elementum sapien scelerisque. Praesent nec mauris arcu. Vivamus vitae vulputate turpis. Phasellus magna ante, egestas quis ullamcorper ac, egestas ut ante. Integer tincidunt risus sit amet fringilla pulvinar. Donec a dui magna. Morbi at est dui. Morbi pharetra a lacus sit amet consectetur. Sed hendrerit augue in tempor bibendum. Quisque nec laoreet nulla. Phasellus ut leo non urna pellentesque semper. Suspendisse a ultrices nulla.
Aenean tempus id justo in pharetra. Donec hendrerit, sem sit amet vulputate condimentum, sapien metus tristique libero, eget semper mauris mi eget magna. Integer tincidunt sem sapien, quis aliquet ex rutrum faucibus. Praesent in fermentum leo. Nulla nec massa tellus. Etiam nisl nisl, accumsan bibendum lorem ut, eleifend vestibulum lectus. Morbi pharetra venenatis lobortis. Nullam volutpat diam nec ipsum volutpat suscipit. Nunc fermentum venenatis erat, eu tempus tortor malesuada ut. Quisque et sollicitudin eros.
Vivamus gravida, erat in ultricies mattis, quam mi molestie massa, in rutrum risus nisi at nulla. Nullam aliquam massa non varius scelerisque. Ut sagittis viverra nunc venenatis elementum. Etiam non nisl nec orci efficitur scelerisque. Integer rhoncus sem sit amet libero suscipit, vel ullamcorper libero aliquam. Aenean non aliquam lorem, finibus semper nibh. Curabitur pharetra finibus massa malesuada suscipit. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Nunc in lacus faucibus ex fringilla ullamcorper vitae a arcu. Duis bibendum libero nisl, vel tincidunt erat molestie sed.
Nunc bibendum diam eget lacus varius faucibus. Mauris a urna metus. In porttitor erat sed tortor euismod facilisis. Vivamus tempor lacinia est. Donec pretium lorem libero, ut scelerisque turpis laoreet in. Sed sapien felis, ultrices a blandit ac, efficitur ut quam. Pellentesque vitae fermentum libero. Fusce finibus fermentum elit, ac egestas mauris rhoncus quis.
Nulla fermentum eros quam, ut pulvinar elit ullamcorper vel. Praesent fringilla elit at augue aliquet, non accumsan velit commodo. Donec dolor augue, luctus in tincidunt a, aliquam sit amet mi. Vivamus ac lorem nunc. Praesent finibus ultricies finibus. Nam blandit eros vitae diam consequat, vitae lobortis neque tempor. Donec dignissim porttitor sem sed sodales. Aenean cursus posuere nibh non molestie. Duis convallis felis non dui dignissim porta eu et turpis. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aenean quis dui porta, sollicitudin tortor at, semper elit. Cras posuere, magna ut dictum ullamcorper, ipsum neque mattis ante, sed ultrices neque nunc vitae nunc. Nulla facilisi.
Aenean molestie vitae odio non accumsan. Mauris erat enim, eleifend ac luctus ut, commodo ut ligula. Maecenas quis mi blandit, dapibus tellus id, congue leo. Vivamus vel felis lobortis, fringilla odio et, suscipit sapien. Integer sit amet tincidunt sapien, eget vestibulum tortor. Duis malesuada dignissim augue, sed pharetra neque volutpat a. Proin urna quam, varius in accumsan vel, sagittis et dui. Proin interdum turpis quis semper congue. Duis in aliquet eros. Morbi sed suscipit justo. Nulla sed ante accumsan nisi tristique dapibus vitae convallis nisl. Pellentesque finibus mauris cursus tempor mollis. Sed libero nulla, congue a tempor a, congue nec purus. Ut pretium gravida tempor. Aliquam erat volutpat.
In ultrices convallis nisl ac egestas. Nam sed libero id ligula posuere suscipit. Curabitur at venenatis elit. Cras erat lacus, blandit non enim ut, ullamcorper tincidunt massa. In ac mauris ultrices, posuere odio eget, finibus elit. Fusce ut diam tempor, laoreet est sit amet, luctus tortor. Phasellus facilisis lorem gravida nisi interdum, vel porta tortor bibendum. Sed nec velit consectetur risus dictum dictum.
Suspendisse quis mi vitae diam pulvinar interdum sit amet id libero. Nam malesuada neque sed nibh dapibus, vitae tincidunt lectus ornare. Maecenas ut leo vitae ipsum vulputate laoreet. Proin erat quam, lacinia in libero sit amet, placerat lacinia ligula. Nullam sit amet tempor tortor. Duis gravida, tortor eu sagittis vehicula, odio massa consectetur leo, pulvinar pretium diam tellus quis felis. Vivamus leo augue, dictum eget lorem quis, vestibulum volutpat augue. Donec turpis lorem, venenatis quis nulla quis, mollis mattis dolor. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.
Suspendisse in turpis convallis, dictum lacus quis, commodo lacus. Nullam scelerisque diam arcu, id porta ligula dapibus ut. Donec vel tempor nisi. Quisque erat lorem, convallis quis suscipit vitae, mattis nec nibh. Sed tincidunt, urna nec laoreet congue, magna ex suscipit magna, id ullamcorper sapien quam at nulla. Maecenas mollis aliquam orci. Quisque egestas ligula id augue pharetra rutrum. Aliquam vulputate elementum ultricies. Sed nec massa sed ante faucibus vehicula nec sit amet nisl.
Etiam volutpat augue eros. Etiam eleifend nisl nisi, nec venenatis turpis tristique posuere. Praesent elementum tellus lectus, ac elementum enim hendrerit at. Ut eleifend ipsum at nulla congue, a semper magna porta. Mauris imperdiet arcu ac lectus interdum congue. Sed posuere pharetra ante non varius. Sed vitae porta orci. Cras sed rutrum purus, eget venenatis metus. Sed ultrices ipsum dolor, ac aliquet ligula dignissim quis. Duis fringilla quam sed dolor fringilla, ut vulputate felis feugiat.
Cras velit diam, pharetra at mollis in, tristique sed tellus. Pellentesque tempor, enim id fermentum interdum, mi lectus blandit quam, ac feugiat eros lectus quis enim. Ut ut pharetra diam, quis convallis lacus. Aenean at tincidunt quam. Donec a libero id metus blandit efficitur ac ac urna. Cras lobortis elementum lorem, dictum lobortis odio placerat a. Vivamus maximus enim eros, iaculis vehicula augue hendrerit at. Vivamus vestibulum orci arcu, vitae fermentum dui volutpat quis. Donec sapien nibh, pellentesque sed sapien sed, semper dictum elit. In ut laoreet neque. Nam ac leo commodo, cursus nisi in, ultrices dui. Morbi non ante mi.
In iaculis, libero in imperdiet mattis, nunc purus laoreet nisl, eu porta neque leo quis elit. Quisque dictum auctor quam. Nulla viverra pharetra est, in accumsan dolor. Maecenas at pharetra ex. Suspendisse hendrerit posuere est scelerisque malesuada. Phasellus sed nisi eget tellus semper placerat. Nullam venenatis dictum imperdiet. Nulla ac pellentesque tortor, sit amet rutrum nisi.
Nulla pulvinar hendrerit ex, nec convallis risus ullamcorper non. Nam commodo, ex ut malesuada dignissim, elit massa sollicitudin libero, tristique varius tellus dolor eu tortor. Integer imperdiet, magna vel rhoncus posuere, diam augue sollicitudin felis, nec molestie orci felis ultricies nisi. Fusce consequat ac mauris a egestas. Donec non ultricies turpis. Duis eu ex non nisl mollis euismod euismod id nulla. Phasellus non velit vel nibh maximus tempor. Pellentesque ac vehicula lectus. Integer laoreet diam libero, eu bibendum tellus laoreet porta. Donec tincidunt orci purus. Integer malesuada erat sit amet nunc vestibulum bibendum.
Nulla facilisi. Ut vitae justo eu neque dignissim blandit in at tellus. Morbi viverra magna odio, nec laoreet felis egestas quis. Praesent id vulputate tortor, et gravida purus. Donec ac nisi vitae lorem blandit vestibulum. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Praesent metus leo, posuere vitae pharetra at, placerat et nibh. Nullam vitae metus nec erat mollis semper.
Morbi eleifend velit eget ornare gravida. Praesent tincidunt et leo in ullamcorper. Sed semper cursus velit ut condimentum. Aenean libero lectus, laoreet in est nec, faucibus porttitor odio. Donec ut turpis id erat viverra mollis. Fusce semper fringilla elit ut sodales. Nunc porttitor eget nunc nec pretium. Vivamus egestas felis vel accumsan porta. Suspendisse rutrum diam nec est placerat feugiat. Curabitur tortor tellus, porta et eleifend sed, vulputate tempus odio. Ut imperdiet ipsum ullamcorper eros luctus interdum. Nullam consequat at velit vitae aliquet. Maecenas venenatis convallis elit, in sagittis dolor faucibus sed. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Integer efficitur lorem suscipit quam euismod placerat.
Aenean et quam dapibus massa molestie mollis viverra eget magna. Pellentesque malesuada ultrices tortor, quis bibendum massa consequat nec. Nunc sagittis lobortis semper. Sed porta venenatis est non lacinia. Nam finibus volutpat neque lacinia tempus. Nulla facilisi. Cras blandit justo nec sem fringilla, non viverra nunc finibus. Mauris luctus tempus augue, id mattis est maximus ac. Integer viverra sollicitudin sapien a hendrerit. Ut auctor tristique sapien at molestie. Fusce sodales congue libero eu scelerisque. Proin sollicitudin turpis eu magna gravida maximus. Nulla nec nunc id sapien feugiat iaculis. Sed a erat eget ante sagittis vulputate at non mi. Cras faucibus nibh aliquet, dictum risus ut, rutrum nunc.
Integer arcu elit, mattis ut dapibus ut, commodo ac leo. Cras fermentum urna vitae tellus dictum tempus. Maecenas est justo, luctus vitae rhoncus vitae, convallis in lorem. Fusce ac faucibus lorem. Etiam ac lorem quis nisl gravida gravida. Donec eu scelerisque enim. Etiam suscipit elit non egestas semper. Maecenas ac tellus quis augue pretium laoreet. Nulla at mauris et augue imperdiet varius.
Nulla congue mi urna, eget auctor nunc placerat non. Vestibulum ac felis et quam rhoncus tincidunt. Donec bibendum pellentesque ipsum, eget vehicula tortor pretium eget. Donec imperdiet facilisis elit quis aliquet. Morbi non mauris venenatis, bibendum nulla at, ornare nunc. Sed diam erat, tincidunt sed ex quis, condimentum sollicitudin tortor. Suspendisse potenti. Phasellus molestie lectus a neque vulputate, id ultrices risus auctor. Integer cursus condimentum arcu vitae posuere.
Nam porta velit aliquam, porttitor felis sed, faucibus quam. Nunc in turpis eget nibh ornare lacinia. In gravida vestibulum lacus, in cursus metus. Maecenas in odio sit amet nunc porttitor sodales. Praesent eget interdum nisi, eu auctor diam. Mauris commodo metus sit amet laoreet tincidunt. Nulla nec aliquet elit. In nec turpis pellentesque, blandit turpis non, imperdiet tellus.
Sed augue nunc, blandit eu nunc ac, convallis vestibulum magna. Vivamus laoreet, nisl ac gravida sollicitudin, mauris dui ultricies nisl, vel varius eros felis vel nunc. Morbi consectetur consectetur nulla, id finibus ex ultricies et. Aliquam vitae aliquam justo. Nam vehicula elit ac sapien convallis vestibulum. Fusce id ullamcorper diam, at porttitor lorem. Duis eget fermentum metus, sed cursus justo. Maecenas aliquam vestibulum ullamcorper.
Mauris vestibulum tortor in consectetur fringilla. Pellentesque eu sapien interdum, sollicitudin neque vel, ornare sem. Donec sed ullamcorper lectus, ut semper lacus. Donec venenatis et libero non porta. Praesent maximus dolor nisi, placerat mollis ante consequat eget. In hac habitasse platea dictumst. Suspendisse aliquam dui eu sodales maximus. Aenean nulla diam, commodo non eros sed, sodales pellentesque enim. Nunc et nisi sit amet metus blandit consequat vel eget magna. Phasellus feugiat iaculis placerat. Ut hendrerit odio in ex ullamcorper accumsan. 
"""
NAMES = [
    "Norman Lodge",
    "Isabelle Senior",
    "Gerald Boyd",
    "April Hull",
    "Stefan Hooper",
    "Nicola Clark",
    "Kerry Gordon",
    "Manjit Osborne",
    "Kylie Bowles",
    "Daisy Crompton",
    "Terence Wadsworth",
    "Anton Goode",
    "Debra Draper",
    "Anthony Harvey",
    "Rose Chadwick",
    "Josh Baker",
    "Camilla Hawkes",
    "Glynis Owen",
    "Jerry Crossley",
    "Kiran Wilde",
    "Stacy Bell",
    "Isaac Britton",
    "Karin Sullivan",
    "Fraser Fisher",
    "Phillip Cook",
    "Estelle Calvert",
    "Rowan Howard",
    "Gerard Clegg",
    "Stacey Gardner",
    "Gemma Wiltshire",
    "Murray Simmonds",
    "Tom Carter",
    "Josie Daley",
    "Polly Poole",
    "Yasmin Johnston",
    "Julia Priestley",
    "Lyndsey Gregory",
    "Monica Osborn",
    "Violet Wharton",
    "Ivan Dobson",
    "Veronica Carey",
    "Serena Hoyle",
    "Callum Love",
    "Gregory Briggs",
    "Gavin Welsh",
    "Rupert Preston",
    "Lynda Walmsley",
    "Luis Barker",
    "Winston Wilkins",
    "Arron McDonald",
]

COMMIT_NAMES = [
    "Ooops, forgot a mistake",
    "Accidentally deleted an important file",
    "Add functionality",
    "Refactor code",
    "Clean code",
    "Clean code from other people",
    "Bug found",
    "Bug fixed",
    "Hell yeah, this is good code",
    "Forgot this piece of code",
    "Forgot this piece of code a second time",
    "Fix",
    "Hotfix",
    "Hotfix (merge immediatly)",
]


def generate_random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


files = []
shutil.rmtree("ctf")
shutil.rmtree("ctf-base")
os.mkdir("ctf")

g = git.Git("ctf")
g.execute(["git", "init", "-b", "main"])
g.execute(["git", "config", "--local", "commit.gpgsign", "false"])
repo = Repo("ctf")

# Create the first commit that will be the base for the game
Path("ctf/hey").touch()
with open("ctf/.gitignore", "w") as fout:
    fout.write(
        """
.ash_history
.gitconfig
.ssh/
    """
    )
repo.git.add("hey")
repo.git.add(".gitignore")
repo.git.commit(
    "-a",
    "-m",
    f"This looks a bit empty. You could try this remote: {REMOTE}",
    author="root <root@ctf>",
)

shutil.copytree("ctf", "ctf-base")

# Add the importants commit for text
with open(f"ctf/text.txt", "w") as fout:
    fout.write(TEXT)

repo.git.add("text.txt")
repo.git.commit(
    "-a",
    "-m",
    "Adding some text",
    author=f"{NAMES[PEOPLE_MAIN]} <{NAMES[PEOPLE_MAIN].split(' ')[0]}.{NAMES[PEOPLE_MAIN].split(' ')[1]}@ctf>",
)


# Now create a bunch of shit
for i in range(50):
    name = random.choice(NAMES)
    message = random.choice(COMMIT_NAMES)
    p = random.randint(0, 1)
    if not len(files):
        p = 0
    if p:
        filename = random.choice(files)
    else:
        filename = generate_random_string(random.randint(3, 15))
        files.append(filename)
    with open(f"ctf/{filename}.txt", "wb") as fout:
        fout.write(os.urandom(1024))
    repo.git.add(f"{filename}.txt")
    repo.git.commit(
        "-a",
        "-m",
        f"{message}",
        author=f"{name} <{name.split(' ')[0]}.{name.split(' ')[1]}@ctf>",
    )

    p = random.random()
    if p >= 0.8 and name != NAMES[PEOPLE_END]:
        random_line = LINE
        while random_line == LINE:
            random_line = random.randint(0, N_LINES - 1)
        new_text = ""
        with open("ctf/text.txt", "r") as f:
            for i, line in enumerate(f):
                if i != random_line:
                    new_text += line
                else:
                    new_text += line[1:]
        with open("ctf/text.txt", "w") as f:
            f.write(new_text)

        repo.git.add("text.txt")
        repo.git.commit(
            "-a",
            "-m",
            f"{message}",
            author=f"{name} <{name.split(' ')[0]}.{name.split(' ')[1]}@ctf>",
        )

new_text = ""
with open("ctf/text.txt", "r") as f:
    for i, line in enumerate(f):
        if i != LINE:
            new_text += line
        else:
            new_text += line[1:]
with open("ctf/text.txt", "w") as f:
    f.write(new_text)

repo.git.add("text.txt")
repo.git.commit(
    "-a",
    "-m",
    f"Modifying {NAMES[PEOPLE_MAIN]} stupid code",
    author=f"{NAMES[PEOPLE_END]} <{NAMES[PEOPLE_END].split(' ')[0]}.{NAMES[PEOPLE_END].split(' ')[1]}@ctf>",
)

for i in range(50):
    name = random.choice(NAMES)
    message = random.choice(COMMIT_NAMES)
    p = random.randint(0, 1)
    if not len(files):
        p = 0
    if p:
        filename = random.choice(files)
    else:
        filename = generate_random_string(random.randint(3, 15))
        files.append(filename)
    with open(f"ctf/{filename}.txt", "wb") as fout:
        fout.write(os.urandom(1024))
    repo.git.add(f"{filename}.txt")
    repo.git.commit(
        "-a",
        "-m",
        f"{message}",
        author=f"{name} <{name.split(' ')[0]}.{name.split(' ')[1]}@ctf>",
    )

    p = random.random()
    if p >= 0.8 and name != NAMES[PEOPLE_END]:
        random_line = LINE
        while random_line == LINE:
            random_line = random.randint(0, N_LINES - 1)
        new_text = ""
        with open("ctf/text.txt", "r") as f:
            for i, line in enumerate(f):
                if i != random_line:
                    new_text += line
                else:
                    new_text += line[1:]
        with open("ctf/text.txt", "w") as f:
            f.write(new_text)

        repo.git.add("text.txt")
        repo.git.commit(
            "-a",
            "-m",
            f"{message}",
            author=f"{name} <{name.split(' ')[0]}.{name.split(' ')[1]}@ctf>",
        )

# Add the two importants commits
with open(f"ctf/secrets.txt", "w") as fout:
    fout.write(
        f"Someone modified my precious functions on line {LINE+1} of the text.txt file. You should look at the branch of this moron, he really doesn't get what he is doing\n"
    )

repo.git.add("secrets.txt")
repo.git.commit(
    "-a",
    "-m",
    "Adding some info",
    author=f"{NAMES[PEOPLE_MAIN]} <{NAMES[PEOPLE_MAIN].split(' ')[0]}.{NAMES[PEOPLE_MAIN].split(' ')[1]}@ctf>",
)

g.execute(["git", "rm", "secrets.txt"])
repo.git.commit(
    "-a",
    "-m",
    "Ooops, this was actually a secret",
    author=f"{NAMES[PEOPLE_MAIN]} <{NAMES[PEOPLE_MAIN].split(' ')[0]}.{NAMES[PEOPLE_MAIN].split(' ')[1]}@ctf>",
)

# Now create a bunch of shit
for i in range(100):
    name = random.choice(NAMES)
    message = random.choice(COMMIT_NAMES)
    p = random.randint(0, 1)
    if not len(files):
        p = 0
    if p:
        filename = random.choice(files)
    else:
        filename = generate_random_string(random.randint(3, 15))
        files.append(filename)
    with open(f"ctf/{filename}.txt", "wb") as fout:
        fout.write(os.urandom(1024))
    repo.git.add(f"{filename}.txt")
    repo.git.commit(
        "-a",
        "-m",
        f"{message}",
        author=f"{name} <{name.split(' ')[0]}.{name.split(' ')[1]}@ctf>",
    )

    p = random.random()
    if p >= 0.8 and name != NAMES[PEOPLE_END]:
        random_line = LINE
        while random_line == LINE:
            random_line = random.randint(0, N_LINES - 1)
        new_text = ""
        with open("ctf/text.txt", "r") as f:
            for i, line in enumerate(f):
                if i != random_line:
                    new_text += line
                else:
                    new_text += line[1:]
        with open("ctf/text.txt", "w") as f:
            f.write(new_text)

        repo.git.add("text.txt")
        repo.git.commit(
            "-a",
            "-m",
            f"{message}",
            author=f"{name} <{name.split(' ')[0]}.{name.split(' ')[1]}@ctf>",
        )


name = random.choice(NAMES)
message = f"Sometimes {NAMES[PEOPLE_MAIN]} is not very careful with what he commits. Cleaning after him. Again !"
filename = generate_random_string(random.randint(3, 15))
files.append(filename)
with open(f"ctf/{filename}.txt", "wb") as fout:
    fout.write(os.urandom(1024))
repo.git.add(f"{filename}.txt")
repo.git.commit(
    "-a",
    "-m",
    f"{message}",
    author=f"{name} <{name.split(' ')[0]}.{name.split(' ')[1]}@ctf>",
)

# Now create chit branches for everyone
for name in NAMES:
    if name != NAMES[PEOPLE_END]:
        files = []
        g.execute(["git", "checkout", "main"])
        g.execute(
            ["git", "checkout", "-b", f"{name.split(' ')[0]}{name.split(' ')[1]}"]
        )
        for i in range(50):
            name = random.choice(NAMES)
            message = random.choice(COMMIT_NAMES)
            p = random.randint(0, 1)
            if not len(files):
                p = 0
            if p:
                filename = random.choice(files)
            else:
                filename = generate_random_string(random.randint(3, 15))
                files.append(filename)
            with open(f"ctf/{filename}.txt", "wb") as fout:
                fout.write(os.urandom(1024))
            repo.git.add(f"{filename}.txt")
            repo.git.commit(
                "-a",
                "-m",
                f"{message}",
                author=f"{name} <{name.split(' ')[0]}.{name.split(' ')[1]}@ctf>",
            )

g.execute(["git", "checkout", "main"])
name = NAMES[PEOPLE_END]
g.execute(["git", "checkout", "-b", f"{name.split(' ')[0]}{name.split(' ')[1]}"])
for i in range(25):
    name = random.choice(NAMES)
    message = random.choice(COMMIT_NAMES)
    p = random.randint(0, 1)
    if not len(files):
        p = 0
    if p:
        filename = random.choice(files)
    else:
        filename = generate_random_string(random.randint(3, 15))
        files.append(filename)
    with open(f"ctf/{filename}.txt", "wb") as fout:
        fout.write(os.urandom(1024))
    repo.git.add(f"{filename}.txt")
    repo.git.commit(
        "-a",
        "-m",
        f"{message}",
        author=f"{name} <{name.split(' ')[0]}.{name.split(' ')[1]}@ctf>",
    )

Path("ctf/token").touch()
with open("ctf/token", "w") as f:
    f.write(TOKEN)

repo.git.add("token")
sha_1 = repo.git.commit(
    "-a",
    "-m",
    "Some modifications",
    author=f"{NAMES[PEOPLE_END]} <{NAMES[PEOPLE_END].split(' ')[0]}.{NAMES[PEOPLE_END].split(' ')[1]}@ctf>",
)
sha_1 = sha_1.split("]")[0].split(" ")[1]

g.execute(["git", "rm", "token"])
sha_2 = repo.git.commit(
    "-a",
    "-m",
    "Remove the modifications",
    author=f"{NAMES[PEOPLE_END]} <{NAMES[PEOPLE_END].split(' ')[0]}.{NAMES[PEOPLE_END].split(' ')[1]}@ctf>",
)
sha_2 = sha_2.split("]")[0].split(" ")[1]

for i in range(25):
    name = random.choice(NAMES)
    message = random.choice(COMMIT_NAMES)
    p = random.randint(0, 1)
    if not len(files):
        p = 0
    if p:
        filename = random.choice(files)
    else:
        filename = generate_random_string(random.randint(3, 15))
        files.append(filename)
    with open(f"ctf/{filename}.txt", "wb") as fout:
        fout.write(os.urandom(1024))
    repo.git.add(f"{filename}.txt")
    repo.git.commit(
        "-a",
        "-m",
        f"{message}",
        author=f"{name} <{name.split(' ')[0]}.{name.split(' ')[1]}@ctf>",
    )

Path("ctf/end").touch()
repo.git.add("end")
repo.git.commit(
    "-a",
    "-m",
    f"Look difference between commit {sha_1} and {sha_2}",
    author=f"{NAMES[PEOPLE_END]} <{NAMES[PEOPLE_END].split(' ')[0]}.{NAMES[PEOPLE_END].split(' ')[1]}@ctf>",
)


g.execute(["git", "checkout", "main"])
g.execute(["git", "remote", "add", "origin", REMOTE])
g.execute(["git", "push", "--all", "origin", "--force"])
