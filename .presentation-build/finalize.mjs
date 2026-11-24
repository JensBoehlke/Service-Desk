
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const [, , skill, python, artifact, d]=process.argv;
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'artifact_tool_utils.mjs')).href);
const options={
 workspaceDir:d,
 candidatePath:path.join(d,'candidate.pptx'),
 finalPath:path.join(d,'output','ServiceDesk_Projektpraesentation.pptx'),
 pythonExecutable:python,
 integrityValidatorPath:path.join(skill,'inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(skill,'inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit','--require-native-table-slide','14','--require-native-table-slide','15'],
 explicitTotalSlideCount:17,
 requiredNativeTableOwnerSlides:[14,15],
 fontPolicy:{basis:'design',families:['Segoe UI','Segoe UI Symbol']},
 verifyArtifactToolImport:true,
 artifactToolModulePath:artifact,
 receiptPath:path.join(d,'validation.json')
};
const r=await finalizePresentation(options);
console.log(JSON.stringify({finalPath:r.finalPath,receiptPath:r.receiptPath,slideCount:r.slideCount}));
