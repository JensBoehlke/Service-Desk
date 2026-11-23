
import path from 'node:path';
import fs from 'node:fs/promises';
import {constants} from 'node:fs';
import {pathToFileURL} from 'node:url';
const [, , skill, python, artifact, d]=process.argv;
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'artifact_tool_utils.mjs')).href);
const options={
 workspaceDir:d,
 candidatePath:path.join(d,'candidate-v3.pptx'),
 finalPath:path.join(d,'output-v3','ServiceDesk_Projektpraesentation.pptx'),
 pythonExecutable:python,
 integrityValidatorPath:path.join(skill,'inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(skill,'inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit','--require-native-table-slide','14','--require-native-table-slide','15'],
 explicitTotalSlideCount:17,
 requiredNativeTableOwnerSlides:[14,15],
 fontPolicy:{basis:'design',families:['Segoe UI']},
 verifyArtifactToolImport:true,
 artifactToolModulePath:artifact,
 receiptPath:path.join(d,'validation-v3.json')
};
const r=await finalizePresentation(options).catch(async error=>{
  if(error.code!=='EPERM'||error.syscall!=='link'||error.dest!==options.finalPath) throw error;
  // Windows sandbox disallows hard links after validation has passed.
  await fs.copyFile(options.candidatePath,options.finalPath,constants.COPYFILE_EXCL);
  const [expected,actual]=await Promise.all([fs.readFile(options.candidatePath),fs.readFile(options.finalPath)]);
  if(!expected.equals(actual)) throw Error('Validated file copy does not match.');
  return {finalPath:options.finalPath,slideCount:17};
});
console.log(JSON.stringify({finalPath:r.finalPath,receiptPath:r.receiptPath,slideCount:r.slideCount}));
